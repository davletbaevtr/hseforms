from django.shortcuts import render


def main(request):
    return render(request, 'main/main.html')


def myforms(request):
    # проверка авторизован или нет
    # если нет то идет на auth
    return render(request, 'main/myforms.html')
