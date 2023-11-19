from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView

from myforms.models import Survey


def main(request):
    return render(request, 'main/main.html')


class RegisterView(CreateView):
    template_name = 'registration/register.html'
    form_class = UserCreationForm
    success_url = reverse_lazy("myforms")

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


def take_survey(request, unique_id):
    # Получаем опрос по unique_id
    survey = get_object_or_404(Survey, unique_id=unique_id)

    # Получаем все вопросы, связанные с этим опросом, вместе с их опциями
    questions = survey.questions.prefetch_related('options').order_by('number')

    return render(request, 'main/take_survey.html', {'survey': survey, 'questions': questions})
