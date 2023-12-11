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


class CorrectTextAnswerBank(models.Model):
    question = models.ForeignKey(QuestionBank, on_delete=models.CASCADE, related_name='correct_text_answers')
    text_answer = models.TextField()


class Survey(models.Model):
    unique_id = models.UUIDField(default=uuid.uuid4, editable=True, unique=True)  # уникальный id опроса

    # создатель опроса
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='surveys')

    title = models.CharField(max_length=255, default='Название опроса')
    description = models.TextField(default='Описание опроса')

    # обязательна аутентификация, если да, то пользователь делится логином
    is_authentication_required = models.BooleanField(default=False)

    is_quiz = models.BooleanField(default=False) # квиз или нет если да то score активно

    create_datetime = models.DateTimeField(auto_now_add=True)
    update_datetime = models.DateTimeField(auto_now=True)

    max_score = models.IntegerField(default=0)


# это вопрос для опроса, его можно скопировать с банка вопросов либо создать самому в редакторе
class QuestionSurvey(models.Model):
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE, related_name='questions')
    number = models.IntegerField(default=0)
    question = models.TextField()  # название вопроса
    question_type = models.CharField(max_length=20)  # single_choice/text/multi_choice
    is_required = models.BooleanField(default=False)  # обязательный

    # если вопрос текстовый, то правильные текстовые ответы состоят из CorrectTextAnswer
    # если выбор вариантов, то правильный(ые) вариант(ы) состоят из Choices

    # если квиз,
    # то стоимость правильного ответа и стоимость неправильного ответа
    # иначе это поле не используется
    correct_score = models.IntegerField(default=0)
    incorrect_score = models.IntegerField(default=0)

    # можно выбрать либо частичную оценку,
    # либо только одно множество ответов правильное,
    # а все другие множества неправильные
    # при частичной каждый вопрос весит correct_score, а каждая ошибка incorrect_score
    # при одном множестве весь правильный ответ весит correct_score, а все другие весят incorrect_score
    is_partial_eval = models.BooleanField(default=False)


# это для вопроса из опроса ответ
class CorrectTextAnswerSurvey(models.Model):
    question = models.ForeignKey(QuestionSurvey, on_delete=models.CASCADE, related_name='correct_text_answers')
    text_answer = models.TextField()


class ChoiceBank(models.Model):
    question = models.ForeignKey(QuestionBank, on_delete=models.CASCADE, related_name='choices')
    choice = models.CharField(max_length=100)  # название варианта
    is_answer = models.BooleanField(default=False)  # является ли данный вариант ответом


class ChoiceSurvey(models.Model):
    question = models.ForeignKey(QuestionSurvey, on_delete=models.CASCADE, related_name='choices')
    choice = models.CharField(max_length=100)  # название варианта
    is_answer = models.BooleanField(default=False)  # является ли данный вариант ответом
    number = models.IntegerField(default=0)


# создается при каждом прохождении опроса
class UserSurvey(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_responses', null=True)
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE)
    score_sum = models.IntegerField(default=0)


class UserResponse(models.Model):
    user_survey = models.ForeignKey(UserSurvey, on_delete=models.CASCADE, related_name='responses')
    question = models.ForeignKey(QuestionSurvey, on_delete=models.CASCADE)

    response_text = models.TextField()  # если вопрос текстового типа
    selected_options = models.ManyToManyField(ChoiceSurvey)  # иначе

    score = models.IntegerField(default=0)
