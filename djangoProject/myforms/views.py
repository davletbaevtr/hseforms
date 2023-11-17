from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from djangoProject.myforms.models import Survey


@login_required
def myforms(request):
    return render(request, 'myforms/myforms.html')


@login_required
def create(request):
    survey = Survey.objects.create()
    return redirect('edit_survey', unique_id=survey.unique_id)


def edit(request, unique_id):
    survey = get_object_or_404(Survey, unique_id=unique_id)

    # Проверка, является ли пользователь создателем опроса
    if request.user != survey.creator:
        # Возврат ошибки или перенаправление, если пользователь не создатель
        return redirect('access_error_page')

    # Логика редактирования опроса

    return render(request, 'myforms/edit_survey.html', {'survey': survey})
