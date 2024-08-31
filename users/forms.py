from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

import users.models as OTTHER


class RegisterUserForm(UserCreationForm):
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    occupation = forms.ChoiceField(choices=[('athlete', 'Athlete'), ('chef', 'Chef'), ('other', 'Other')])

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'first_name', 'last_name', 'occupation']


class ProfileUpdateForm(forms.ModelForm):
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=False)
    gender = forms.ChoiceField(choices=[('male', 'Male'), ('female', 'Female')], required=False)
    height = forms.IntegerField(validators=[MinValueValidator(0)], help_text="(in cm)", required=False)
    weight = forms.DecimalField(max_digits=5, decimal_places=1,
                                validators=[MinValueValidator(0), MaxValueValidator(999.9)], help_text="(in kg)", required=False)
    sport = forms.CharField(max_length=100, required=False, help_text="Write your preferred sport "
                                                                      "if you are an athlete. If not, skip this part")
    exercise_per_week = forms.ChoiceField(choices=[('none', 'None'), ('light', 'Light (1-2 days per week)'),
                                                   ('moderate', 'Moderate (3-4 days per week)'),
                                                   ('intense', 'Intense (5 or more days per week)')], required=False)
    purpose = forms.ChoiceField(choices=[('lose_weight', 'Weight Loss'),
                                         ('gain_weight', 'Muscle Gain'),
                                         ('maintain_weight', 'Maintain It')], required=False)
    calories_should_taken = forms.FloatField(required=False, widget=forms.HiddenInput())

    class Meta:
        model = User
        fields = ['date_of_birth', 'gender', 'height', 'weight', 'sport', 'exercise_per_week', 'purpose', 'calories_should_taken']

    def save(self, commit=True):
        user_profile = super().save(commit=False)
        user_profile.date_of_birth = self.cleaned_data['date_of_birth']
        user_profile.gender = self.cleaned_data['gender']
        user_profile.height = self.cleaned_data['height']
        user_profile.weight = self.cleaned_data['weight']
        user_profile.sport = self.cleaned_data['sport']
        user_profile.exercise_per_week = self.cleaned_data['exercise_per_week']
        user_profile.purpose = self.cleaned_data['purpose']
        user_profile.calories_should_taken = self.cleaned_data['calories_should_taken']  # Save calories

        if commit:
            user_profile.save()

        return user_profile
