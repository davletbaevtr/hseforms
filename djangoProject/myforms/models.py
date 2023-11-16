from django.db import models

class Survey(models.Model):
    title = models.CharField(max_length=255) # название опроса
    description = models.TextField() # описание опроса

    def __str__(self):
        return self.title
class Option(models.Model):
    choice = models.CharField(max_length=100) # название для нового варианта
    is_answer = models.BooleanField(default=False) # является ли данный вариант ответом

    def __str__(self):
        return self.choice
class Question(models.Model):
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE, related_name='questions')
    number = 0 # какой вопрос по счету
    question = models.TextField() # название вопроса
    is_checkbox = False # TextField or options Field
    options = models.ManyToManyField(Option, related_name='checkbox_questions') # варианты ответов

    def __str__(self):
        return f'{self.survey.title} - Question {self.number}: {self.question}'
