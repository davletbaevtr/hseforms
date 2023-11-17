from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from djangoProject.myforms.models import Survey


@login_required
def myforms(request):
    return render(request, 'myforms/myforms.html')


@login_required
def create(request):
    survey = Survey.objects.create()
    return redirect('edit_survey', unique_id=survey.unique_id)


def edit(request):
    return render(request, 'myforms/myforms.html')
