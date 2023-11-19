from django.urls import path
from .views import myforms, create, edit

urlpatterns = [
    path('', myforms, name='myforms'),
    path('create', create, name='create_survey'),
    path('edit/<uuid:unique_id>', edit, name='edit_survey')
]
