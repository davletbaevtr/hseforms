from django import forms
from .models import UserResponse
from myforms.models import Option


class UserResponseCheckBoxForm(forms.ModelForm):
    answer = forms.ModelMultipleChoiceField(
        queryset=Option.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = UserResponse
        fields = ['answer']


class UserResponseTextForm(forms.ModelForm):
    answer = forms.CharField(widget=forms.TextInput, required=False)

    class Meta:
        model = UserResponse
        fields = ['answer']
