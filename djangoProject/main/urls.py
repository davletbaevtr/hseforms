from django.urls import path
from .views import main, RegisterView

urlpatterns = [
    path('', main, name='main'),
    path('register', RegisterView.as_view(), name='register'),
]
