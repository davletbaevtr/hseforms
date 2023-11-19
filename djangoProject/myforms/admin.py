from django.contrib import admin
from .models import Survey, Question, Option

admin.site.register(Survey)
admin.site.register(Question)
admin.site.register(Option)
