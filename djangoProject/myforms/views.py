from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def myforms(request):
    return render(request, 'myforms/myforms.html')


def create(request):
    return render(request, '')
