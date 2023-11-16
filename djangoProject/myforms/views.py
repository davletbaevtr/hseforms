from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def myforms(request):
    return render(request, 'myforms/myforms.html')


@login_required
def create(request):
    return render(request, 'myforms/create.html')
