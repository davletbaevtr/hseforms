from django.urls import path
from .views import main, RegisterView, take_survey

urlpatterns = [
    path('', main, name='main'),
    path('register', RegisterView.as_view(), name='register'),
    path('<uuid:unique_id>', take_survey, name='take_survey'),
]
