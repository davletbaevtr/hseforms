from django.contrib import admin
from .models import Survey, Question, Choice, UserSurvey, UserResponse

admin.site.register(Survey)
admin.site.register(Question)
admin.site.register(Choice)
admin.site.register(UserSurvey)
admin.site.register(UserResponse)
