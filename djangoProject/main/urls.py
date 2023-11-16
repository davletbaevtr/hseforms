from django.urls import path
from views import main, myforms, RegisterView

urlpatterns = [
    path('', main, name='main'),
    path('register', RegisterView.as_view(), name='register'),
]
