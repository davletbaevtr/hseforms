from django import forms
from .models import UserResponse, Survey
from .models import ChoiceSurvey


class UserResponseCheckBoxForm(forms.ModelForm):
    answer = forms.ModelMultipleChoiceField(
        queryset=ChoiceSurvey.objects.all(),
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


class SurveyForm(forms.ModelForm):
    class Meta:
        model = Survey
        fields = ['title', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 2}),
        }