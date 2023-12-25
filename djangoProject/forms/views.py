from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse

from .models import Survey
from django.db import transaction
from .forms import SurveyForm
from .models import Survey, UserSurvey, UserResponse, QuestionSurvey, ChoiceSurvey


@login_required
def myforms(request):
    surveys = request.user.surveys.order_by('update_datetime').values('title', 'update_datetime', 'unique_id')

    have_survey = len(surveys) != 0

    context = {
        'have_survey': have_survey,
        'surveys': surveys,
    }

    return render(request, 'forms/myforms.html', context)


@login_required
def create(request):
    survey_form = SurveyForm(request.POST or None)
    if request.method == "POST":
        if survey_form.is_valid():
            form = survey_form.save(commit=False)
            form.creator = request.user
            form.save()
            for key, question_title in request.POST.items():
                if key.startswith('question_text_'):
                    question_number = int(key.split('_')[2])
                    question_type = request.POST.get(f'question_type_{question_number}')
                    all_choices = request.POST.getlist(f'answer_text_{question_number}[]')
                    correct_answers = [int(value) for key, value in request.POST.items() if
                                       key.startswith(f'answer_option_{question_number}')]

                    question = QuestionSurvey()
                    question.question_type = question_type
                    question.survey = form
                    question.question = question_title
                    question.number = question_number
                    question.save()
                    if (question_type != 'text'):
                        cnt = 1
                        for choice in all_choices:
                            choiceModel = ChoiceSurvey()
                            choiceModel.question = question
                            choiceModel.choice = choice
                            if ((cnt - 1) in correct_answers):
                                choiceModel.is_answer = True
                            choiceModel.number = cnt
                            choiceModel.save()
                            cnt += 1
            return render(request, "forms/creation_completed.html", {"survey_title": form.title, 'unique_id': form.unique_id})
    return render(request, 'forms/edit_survey.html', {'survey_form': survey_form})


@login_required
def edit(request, unique_id):
    survey = get_object_or_404(Survey, unique_id=unique_id)

    # Проверка, является ли пользователь создателем опроса
    if request.user != survey.creator:
        # перенаправление на страницу ошибки доступа, если пользователь не создатель
        return render(request, 'forms/access_error.html', {'survey': survey})

    # Логика редактирования(создания) опроса
    return redirect(f'/forms/{survey.unique_id}')


def take_survey(request, unique_id):
    try:
        survey = get_object_or_404(
            # используя prefetch_related подгружаем сразу все вопросы и варианты связанные с опросом
            Survey.objects.prefetch_related(
                'questions__choices',
            ),
            unique_id=unique_id
        )
    except Http404:
        return render(request, 'forms/not_found_survey.html')
    questions = survey.questions.all().order_by('number')

    if survey.is_authentication_required and not request.user.is_authenticated:
        login_url = reverse('login')
        next_url = reverse('take_survey', kwargs={'unique_id': unique_id})
        redirect_url = f"{login_url}?next={next_url}"
        return redirect(redirect_url)

    template_name = 'forms/take_survey.html'

    context = {
        'unique_id': unique_id,
        'survey': survey,
        'questions': questions
    }

    return render(
        request,
        template_name,
        context
    )


def quiz_request_post_parse(request_post, questions, choices_by_question, user_survey) -> int:
    score_sum = 0
    user_responses = []

    # Предварительно загрузим правильные варианты для каждого вопроса
    correct_choices_by_question = {
        q.id: set(choice.number for choice in choices_by_question[q.id] if choice.is_answer)
        for q in questions.values() if q.question_type in ['single_choice', 'multi_choice']
    }

    for el in request_post:
        if el == "csrfmiddlewaretoken":
            continue

        question_id = int(el)
        question = questions[question_id]
        answer = request_post[el]

        user_response = UserResponse(user_survey=user_survey, question=question,
                                     response_text=answer if question.question_type == 'text' else 'None', score=0)

        if question.question_type == 'text':
            # Оценка текстовых ответов
            if answer in [correct_answer.text_answer for correct_answer in question.correct_text_answers.all()]:
                user_response.score = question.correct_score
            else:
                user_response.score = -question.incorrect_score
        elif question.question_type in ['single_choice', 'multi_choice']:
            # Оценка вопросов с выбором

            selected_choices = [choice for choice in choices_by_question[question_id] if str(choice.number) in answer]
            user_response.selected_options = selected_choices

            # partial_eval может быть только у multi_choice вопроса
            if question.is_partial_eval:
                for choice in selected_choices:
                    if choice.is_answer:
                        score_sum += question.correct_score
                        user_response.score += question.correct_score
                    else:
                        score_sum -= question.incorrect_score
                        user_response.score -= question.incorrect_score
            else:
                selected_choice_numbers = set(choice.number for choice in selected_choices)
                # Проверяем совпадает ли сет номеров вариантов с сетом правильных номеров вариантов
                if correct_choices_by_question[question_id] == selected_choice_numbers:
                    score_sum += question.correct_score
                    user_response.score = question.correct_score
                else:
                    score_sum -= question.incorrect_score
                    user_response.score = -question.incorrect_score

        score_sum += user_response.score
        user_responses.append(user_response)

    # Метод bulk_create позволяет одним запросом создать объекты в бд
    created_user_responses = UserResponse.objects.bulk_create(user_responses)

    m2m_relations = []
    for user_response in created_user_responses:
        for choice in user_response.selected_options:
            m2m_relations.append(
                UserResponse.selected_options.through(userresponse_id=user_response.id, choicesurvey_id=choice.id))

    # Здесь through возвращает промежуточную таблицу связи между UserResponse и ChoiceSurvey,
    # которую django создает автоматически(либо мы сами можем её создать)
    UserResponse.selected_options.through.objects.bulk_create(m2m_relations)

    return score_sum


def not_quiz_request_post_parse(request_post, questions, choices_by_question, user_survey):
    user_responses = []
    m2m_relations = []

    for el in request_post:
        if el == "csrfmiddlewaretoken":
            continue

        question_id = int(el)
        question = questions[question_id]
        response_text = request_post[el] if question.question_type == 'text' else 'None'

        user_response = UserResponse(
            user_survey=user_survey,
            question=question,
            response_text=response_text
        )
        user_responses.append(user_response)

        if question.question_type in ['single_choice', 'multi_choice']:
            choice_numbers = [int(choice_number) for choice_number in request_post.getlist(el)]
            m2m_relations.extend([
                (user_response, choice)
                for choice in choices_by_question[question_id]
                if choice.number in choice_numbers
            ])

    # Метод bulk_create позволяет одним запросом создать объекты в бд
    UserResponse.objects.bulk_create(user_responses)

    m2m_objects = [
        UserResponse.selected_options.through(
            userresponse_id=user_response.id,
            choicesurvey_id=choice.id
        )
        for user_response, choice in m2m_relations
    ]

    # Здесь through возвращает промежуточную таблицу связи между UserResponse и ChoiceSurvey,
    # которую django создает автоматически(либо мы сами можем её создать)
    UserResponse.selected_options.through.objects.bulk_create(m2m_objects)


def submit_response(request, unique_id):
    if request.method == "POST":

        survey = get_object_or_404(
            Survey.objects.prefetch_related(
                'questions__choices',
            ),
            unique_id=unique_id
        )

        with transaction.atomic():
            user_survey = UserSurvey(survey=survey)
            if survey.is_authentication_required:
                user_survey.user = request.user
            user_survey.save()

            questions = {q.number: q for q in survey.questions.all()}
            choices_by_question = {q.number: list(q.choices.all()) for q in survey.questions.all()}

            if survey.is_quiz:
                user_survey.score_sum = quiz_request_post_parse(request.POST, questions, choices_by_question,
                                                                user_survey)
                user_survey.save()
            else:
                not_quiz_request_post_parse(request.POST, questions, choices_by_question, user_survey)

        return render(request, "forms/survey_response.html", {"survey_title": survey.title, 'unique_id': unique_id})

    return redirect('take_survey', unique_id=unique_id)
