import uuid
from django.db import models
from django.conf import settings


# это вопрос для банка вопрос
class QuestionBank(models.Model):
    question = models.TextField()  # название вопроса
    # тип вопроса: текстовый ответ, выбор вариантов, множественный выбор
    question_type = models.CharField(max_length=20)  # checkbox/text/multiple

    # если вопрос текстовый, то правильные текстовые ответы состоят из CorrectTextAnswer
    # если выбор вариантов, то правильный(ые) вариант(ы) состоят из Choices

    def __str__(self):
        return f'Question: {self.question}'


class CorrectTextAnswerBank(models.Model):
    question = models.ForeignKey(QuestionBank, on_delete=models.CASCADE, related_name='correct_text_answers')
    text_answer = models.TextField()


class Survey(models.Model):
    unique_id = models.UUIDField(default=uuid.uuid4, editable=True, unique=True)  # уникальный id опроса
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # создатель опроса

    title = models.CharField(max_length=255, default='Название опроса')
    description = models.TextField(default='Описание опроса')

    # обязательна аутентификация, если да, то пользователь делится логином
    is_authentication_required = models.BooleanField(default=False)

    is_quiz = models.BooleanField(default=False) # квиз или нет если да то score активно

    create_datetime = models.DateTimeField(auto_now_add=True)
    update_datetime = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


# это вопрос для опроса, его можно скопировать с банка вопросов либо создать самому в редакторе
class QuestionSurvey(models.Model):
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE, related_name='questions')
    number = models.IntegerField(default=0)
    question = models.TextField()  # название вопроса
    # тип вопроса: текстовый ответ, выбор вариантов, множественный выбор
    question_type = models.CharField(max_length=20)  # checkbox/text/multiple
    is_required = models.BooleanField(default=False)  # обязательный

    # если вопрос текстовый, то правильные текстовые ответы состоят из CorrectTextAnswer
    # если выбор вариантов, то правильный(ые) вариант(ы) состоят из Choices

    # если квиз и текстовый ответ либо выбор варианта,
    # то стоимость правильного ответа и стоимость неправильного ответа
    correct_score = models.IntegerField(default=0)
    incorrect_score = models.IntegerField(default=0)

    # иначе это поле не используется
    def __str__(self):
        return f'Question: {self.question}'


# это для вопроса из опроса ответ
class CorrectTextAnswerSurvey(models.Model):
    question = models.ForeignKey(QuestionSurvey, on_delete=models.CASCADE, related_name='correct_text_answers')
    text_answer = models.TextField()


class ChoiceBank(models.Model):
    question = models.ForeignKey(QuestionBank, on_delete=models.CASCADE, related_name='choices')
    choice = models.CharField(max_length=100)  # название варианта
    is_answer = models.BooleanField(default=False)  # является ли данный вариант ответом

    def __str__(self):
        return self.choice


class ChoiceSurvey(models.Model):
    question = models.ForeignKey(QuestionSurvey, on_delete=models.CASCADE, related_name='choices')
    choice = models.CharField(max_length=100)  # название варианта
    is_answer = models.BooleanField(default=False)  # является ли данный вариант ответом
    number = models.IntegerField(default=0)

    # если квиз с множественным выбором, то стоимость правильного и неправильного варианта,
    # то есть считается частичный ответ и подсчитывается стоимость
    correct_score = models.IntegerField(default=0)
    incorrect_score = models.IntegerField(default=0)
    # иначе эти поля не используется

    def __str__(self):
        return self.choice


# создается при каждом прохождении опроса
class UserSurvey(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE)
    score_sum = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.user.name} - {self.survey.title}'


class UserResponse(models.Model):
    user_survey = models.ForeignKey(UserSurvey, on_delete=models.CASCADE, related_name='responses')
    question = models.ForeignKey(QuestionSurvey, on_delete=models.CASCADE)

    response_text = models.TextField()  # если вопрос текстового типа
    selected_options = models.ManyToManyField(ChoiceSurvey)  # иначе

    score = models.IntegerField(default=0)

    def __str__(self):
        selected_options_str = ', '.join([option.choice for option in self.selected_options.all()])
        return f'{self.user_survey.user.name} - {self.user_survey.survey.title} - {self.question.question} - {selected_options_str}'
