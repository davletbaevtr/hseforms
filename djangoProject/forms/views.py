from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from .models import Survey
from .forms import SurveyForm
from .models import Survey, UserSurvey, UserResponse


@login_required
def myforms(request):
    return render(request, 'forms/myforms.html')


@login_required
def create(request):
    survey = Survey()
    survey.creator = request.user
    survey.save()
    survey_form = SurveyForm(request.POST or None)
    if request.method == "POST":
        if survey_form.is_valid():
            survey_form.save()
            return redirect('edit_survey', unique_id=survey.unique_id)
    return render(request, 'forms/create_survey.html', {'survey_form': survey_form})


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

    # проверить работу
    if survey.is_authentication_required:
        if not request.user.is_authenticated:
            return redirect('login')

    if request.method == "POST":
        print(request.POST)
        user_survey = UserSurvey()

        if survey.is_authentication_required:
            user_survey.user = request.user

        user_survey.survey = survey

        questions = survey.questions.all().order_by('number')
        request_post = request.POST
        for el in request_post:
            # Excluding csrf token
            if el == "csrfmiddlewaretoken":
                continue
            question = questions[el]
            if question.question_type == 'text':
                user_response = UserResponse(
                    user_survey=survey,
                    question=question,
                    response_text=request_post.get_list(el)
                )
            else:
                pass

        user_survey.save()

        return render(request, "forms/survey_response.html", {"survey": survey})
    else:
        return redirect('take_survey', unique_id=unique_id)


