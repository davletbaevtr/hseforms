from django.shortcuts import render
from django.contrib.auth.decorators import login_required


def main(request):
    return render(request, 'main/main.html')


@login_required
def myforms(request):
    # проверка авторизован или нет
    # если нет то идет на auth
    return render(request, 'main/myforms.html')
