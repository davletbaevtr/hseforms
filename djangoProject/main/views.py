from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views.generic import CreateView


def main(request):
    return render(request, 'main/main.html')


@login_required
def myforms(request):
    # проверка авторизован или нет
    # если нет то идет на auth
    return render(request, 'main/myforms.html')


class RegisterView(CreateView):
    template_name = 'registration/register.html'
    form_class = UserCreationForm
    success_url = reverse_lazy("myforms")

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
