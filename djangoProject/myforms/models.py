import uuid
from django.db import models


class Survey(models.Model):
    unique_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)  # уникальный id опроса

    title = models.CharField(max_length=255)  # название опроса
    description = models.TextField()  # описание опроса

    def __str__(self):
        return self.title


class Question(models.Model):
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE, related_name='questions')
    number = 0  # какой вопрос по счету
    question = models.TextField()  # название вопроса
    is_checkbox = False  # TextField or options Field

    def __str__(self):
        return f'{self.survey.title} - Question {self.number}: {self.question}'


class Option(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='question')
    choice = models.CharField(max_length=100)  # название для нового варианта
    is_answer = models.BooleanField(default=False)  # является ли данный вариант ответом

    def __str__(self):
        return self.choice
