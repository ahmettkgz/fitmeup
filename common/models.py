from datetime import date
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator
from django.db import models


class BasePerson(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    occupation = models.CharField(max_length=100)
    date_of_birth = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=10, choices=[('male', 'Male'), ('female', 'Female')], blank=True, null=True)
    height = models.IntegerField(validators=[MinValueValidator(0)], blank=True, null=True)
    weight = models.DecimalField(max_digits=5, decimal_places=1,
                                 validators=[MinValueValidator(0), MaxValueValidator(999.9)], blank=True, null=True)
    PURPOSE_CHOICES = [
        ('gain_weight', 'Gaining Weight'),
        ('lose_weight', 'Losing Weight'),
        ('maintain_weight', 'Maintaining Weight'),
    ]
    purpose = models.CharField(max_length=100, choices=PURPOSE_CHOICES, blank=True, null=True)
    EXERCISE_CHOICES = [
        ('none', 'None'),
        ('light', 'Light (1-2 days per week)'),
        ('moderate', 'Moderate (3-4 days per week)'),
        ('intense', 'Intense (5 or more days per week)'),
    ]
    exercise_per_week = models.CharField(max_length=100, choices=EXERCISE_CHOICES, blank=True, null=True)

    def check_profile_completion(self):
        if self.height is None or self.weight is None or self.date_of_birth is None or \
                self.gender is None or self.purpose is None or self.exercise_per_week is None:
            return False

        return True

    @property
    def calculate_age(self):
        today = date.today()
        age = today - self.date_of_birth
        return age.days // 365

    class Meta:
        abstract = True

    @property
    def calculate_calories(self):
        if self.check_profile_completion():
            if self.gender == 'male':
                bmr = 88.362 + (13.397 * float(self.weight)) + (4.799 * self.height) - (
                        5.677 * (self.calculate_age / 365.25))
            else:
                bmr = 447.593 + (9.247 * float(self.weight)) + (3.098 * self.height) - (
                        4.330 * (self.calculate_age / 365.25))

            activity_multiplier = {
                'none': 1.2,  # Sedentary
                'light': 1.375,  # Lightly active
                'moderate': 1.55,  # Moderately active
                'intense': 1.725,  # Very active
            }

            purpose_modifier = {
                'gain_weight': 1.0,
                'lose_weight': 0.8,
                'maintain_weight': 0.9,
            }

            activity_multiplier_value = activity_multiplier[self.exercise_per_week]
            purpose_modifier_value = purpose_modifier[self.purpose]

            return bmr * activity_multiplier_value * purpose_modifier_value

        else:
            return None

    @property
    def calculate_macros(self):
        if self.check_profile_completion() and self.calculate_calories > 0:
            protein_per_kg = 1.2

            purpose_protein = {
                'lose_weight': 1.0,
                'gain_weight': 1.2,
                'maintain_weight': 1.1,
            }

            purpose = self.purpose
            if purpose not in purpose_protein:
                return None

            protein_multiplier = purpose_protein[purpose]
            total_protein = protein_multiplier * float(self.weight)

            purpose_percentages = {
                'lose_weight': {'carbs': 30, 'fats': 30},
                'gain_weight': {'carbs': 50, 'fats': 20},
                'maintain_weight': {'carbs': 40, 'fats': 30},
            }

            purpose_ratios = purpose_percentages[purpose]
            carbs_percentage = purpose_ratios['carbs']
            fats_percentage = purpose_ratios['fats']

            total_protein = protein_per_kg * float(self.weight)
            protein_calories = total_protein * 4  # 4 calories per gram of protein
            total_calories = self.calculate_calories

            carbs_calories = (carbs_percentage / 100) * total_calories
            fats_calories = (fats_percentage / 100) * total_calories

            total_carbs = carbs_calories / 4  # 4 calories per gram of carbohydrates
            total_fats = fats_calories / 9  # 9 calories per gram of fats

            return {
                'protein': total_protein,
                'carbs': total_carbs,
                'fats': total_fats,
            }
        else:
            return None
