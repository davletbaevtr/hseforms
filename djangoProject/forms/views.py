from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from .models import Survey
from .forms import SurveyForm
from .models import Survey, UserSurvey, UserResponse, QuestionSurvey, ChoiceSurvey


@login_required
def myforms(request):
    return render(request, 'forms/myforms.html')


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
                    question_number = int(key.split('_')[2])-1
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
                        cnt = 0
                        for choice in all_choices:
                            choiceModel = ChoiceSurvey()
                            choiceModel.question = question
                            choiceModel.choice = choice
                            if (cnt in correct_answers):
                                choiceModel.is_answer = True
                            choiceModel.number = cnt
                            choiceModel.save()
                            cnt += 1
            # return redirect('edit_survey', unique_id=form.unique_id)
    return render(request, 'forms/edit_survey.html', {'survey_form': survey_form})


@login_required
def edit(request, unique_id):
    survey = get_object_or_404(Survey, unique_id=unique_id)
    # обработать ошибку

    # Проверка, является ли пользователь создателем опроса
    if request.user != survey.creator:
        # перенаправление на страницу ошибки доступа, если пользователь не создатель
        return redirect('access_error_page')

    # Логика редактирования(создания) опроса

    return render(request, 'forms/edit_survey.html', {'survey': survey})


def take_survey(request, unique_id):
    survey = get_object_or_404(Survey, unique_id=unique_id)

    # проверить работу
    if survey.is_authentication_required:
        if not request.user.is_authenticated:
            return redirect('login')

    questions_data = []
    for question in survey.questions.all().order_by('number'):
        choices = None if question.question_type == 'text' else question.choices.all().order_by('number')
        questions_data.append({
            'question': question,
            'choices': choices
        })

    context = {
        'survey': survey,
        'unique_id': unique_id,
        'questions_data': questions_data
    }

    return render(request, 'forms/take_survey.html', context)


def submit_response(request, unique_id):
    survey = get_object_or_404(Survey, unique_id=unique_id)
    survey_is_quiz = survey.is_quiz

    # проверить работу
    if survey.is_authentication_required:
        if not request.user.is_authenticated:
            return redirect('login')

    if request.method == "POST":
        user_survey = UserSurvey(survey=survey)

        if survey.is_authentication_required:
            user_survey.user = request.user

        user_survey.save()

        questions = survey.questions.all()
        request_post = request.POST
        score_sum = 0
        for el in request_post:
            # Excluding csrf token
            if el == "csrfmiddlewaretoken":
                continue
            question = questions.get(number=int(el))
            user_response = UserResponse(user_survey=user_survey, question=question)
            user_response.save()
            answer = request_post[el]
            if question.question_type == 'text':
                user_response.response_text = answer
                if survey_is_quiz:
                    if answer in question.correct_text_answers.all():
                        question_correct_score = question.correct_score
                        user_response.score = question_correct_score
                        score_sum += question_correct_score
                    else:
                        question_incorrect_score = question.incorrect_score
                        user_response.score = question_incorrect_score
                        score_sum -= question_incorrect_score
            elif question.question_type in ['checkbox', 'multiple']:
                for choice_number in answer:
                    choice = question.choices.get(number=choice_number)
                    user_response.selected_options.add(choice)
                    if survey_is_quiz:
                        choice_score = choice.score
                        if choice.is_answer:
                            user_response.score = choice_score
                            score_sum += choice_score
                        else:
                            user_response.score = -choice_score
                            score_sum -= choice_score
            user_response.save()

        if survey_is_quiz:
            user_survey.score_sum = score_sum
            user_survey.save()

        return render(request, "forms/survey_response.html", {"survey": survey})
    else:
        return redirect('take_survey', unique_id=unique_id)


