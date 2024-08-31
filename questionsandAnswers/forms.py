from django import forms
from . import widgets
from .models import Question


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['title', 'details', 'recievers', 'date_posted']


class AnswerForm(forms.Form):
    text = forms.CharField(label='', widget=widgets.CustomTextarea)

    class Meta:
        model = Question
        fields = ['author', 'text', 'date_posted']
