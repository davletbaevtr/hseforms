from django.contrib import admin
from .models import Survey, QuestionBank, ChoiceBank, UserSurvey, UserResponse, QuestionSurvey, CorrectTextAnswerBank, QuestionSurvey, ChoiceSurvey, CorrectTextAnswerSurvey

admin.site.register(Survey)
admin.site.register(QuestionBank)
admin.site.register(ChoiceBank)
admin.site.register(UserSurvey)
admin.site.register(UserResponse)
admin.site.register(QuestionSurvey)
admin.site.register(CorrectTextAnswerBank)
admin.site.register(CorrectTextAnswerSurvey)
admin.site.register(ChoiceSurvey)
