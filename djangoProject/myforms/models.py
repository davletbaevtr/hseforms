import uuid
from django.db import models
from django.conf import settings


class Survey(models.Model):
    unique_id = models.UUIDField(default=uuid.uuid4, editable=True, unique=True)  # уникальный id опроса
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # создатель опроса

    title = models.CharField(max_length=255, default='Название опроса')
    description = models.TextField(default='описание опроса')

    def __str__(self):
        return self.title


class Question(models.Model):
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE, related_name='questions')
    number = models.IntegerField(default=0)
    question = models.TextField()  # название вопроса
    is_checkbox = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.survey.title} - Question {self.number}: {self.question}'


class Option(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='options')
    choice = models.CharField(max_length=100)  # название для нового варианта
    is_answer = models.BooleanField(default=False)  # является ли данный вариант ответом

    def __str__(self):
        return self.choice
