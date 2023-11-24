from django.urls import path
from .views import myforms, create, edit, take_survey, submit_response

urlpatterns = [
    path('myforms/', myforms, name='myforms'),
    path('create/', create, name='create_survey'),
    path('edit/<uuid:unique_id>', edit, name='edit_survey'),
    path('<uuid:unique_id>', take_survey, name='take_survey'),
    path('submit/<uuid:unique_id>', submit_response, name='submit_response'),
]
