from django.urls import path
from .views import myforms, create

urlpatterns = [
    path('', myforms, name='myforms'),
    path('create', create, name='create_survey'),
    path('edit/<uuid:unique_id>', name='edit_survey')
]
