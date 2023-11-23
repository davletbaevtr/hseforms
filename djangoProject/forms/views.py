from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from .models import Survey


@login_required
def myforms(request):
    return render(request, 'forms/myforms.html')


@login_required
def create(request):
    survey = Survey()
    survey.creator = request.user
    survey.save()

    return redirect('edit_survey', unique_id=survey.unique_id)


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

    question_data = []
    for question in survey.questions.all():
        choices = list(question.choices.all()) if question.question_type in ['checkbox', 'multiple'] else None
        question_data.append({
            'question': question,
            'choices': choices
        })

    context = {
        'unique_id': unique_id,
        'question_data': question_data
    }

    return render(request, 'forms/take_survey.html', context)
