from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views.generic import View
from django.db.models import Sum
from athletesQuotesApp.models import AthleteQuote
from common.models import BasePerson
from diaryApp.models import WaterEntry
from users.models import Athlete, Chef, Other

# JSVtg+MnuvX0mS7qiQimuQ==jcrUxpvFXQ3xsHYG
# Create your views here.


def calculate_remaining_calories(myperson, total_calories):
    if myperson and myperson.calculate_calories is not None:
        remaining_calories = max(myperson.calculate_calories - total_calories, 0)
    else:
        remaining_calories = 0
    return remaining_calories


class IndexView(View):

    def get(self, request):
        return render(request, "index.html")


class DiaryView(View):

    def get(self, request):
        myperson = None
        total_water = 0  # Default total_water to 0

        if request.user.is_authenticated:
            for my_class in [Athlete, Chef, Other]:
                try:
                    myperson = my_class.objects.get(user=request.user)
                    break
                except my_class.DoesNotExist:
                    pass

            total_water = WaterEntry.objects.filter(user=request.user).aggregate(Sum('glasses'))['glasses__sum']

        random_quote = AthleteQuote.objects.order_by('?').first()

        context = {
            "myperson": myperson,
            "total_water": total_water or 0,
            "random_quote": random_quote,
        }

        return render(request, "diary.html", context=context)

    def post(self, request):
        import requests
        import json

        query = request.POST.get('query')
        api_url = 'https://api.api-ninjas.com/v1/nutrition?query='
        headers = {'X-Api-Key': 'JSVtg+MnuvX0mS7qiQimuQ==jcrUxpvFXQ3xsHYG'}
        api_request = requests.get(api_url + query, headers=headers)

        try:
            api = json.loads(api_request.content)
        except Exception as e:
            api = "There was an error"
            print(e)

        total_calories = sum(item.get('calories', 0) for item in api)

        myperson = None
        total_water = 0  # Default total_water to 0

        if request.user.is_authenticated:
            for my_class in [Athlete, Chef, Other]:
                try:
                    myperson = my_class.objects.get(user=request.user)
                    break
                except my_class.DoesNotExist:
                    pass

            total_water = WaterEntry.objects.filter(user=request.user).aggregate(Sum('glasses'))['glasses__sum']

        random_quote = AthleteQuote.objects.order_by('?').first()

        remaining_calories = calculate_remaining_calories(myperson, total_calories)

        # Calculate total calories taken using BasePerson's method

        context = {
            "myperson": myperson,
            "total_water": total_water or 0,
            "random_quote": random_quote,
            "api": api,
            "total_calories": total_calories,
            "remaining_calories": remaining_calories,
        }

        return render(request, 'diary.html', context=context)


class AddWaterView(LoginRequiredMixin, View):
    login_url = '/login/'  # Set the login URL
    redirect_field_name = 'diary.html'

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            glasses = int(request.POST.get('glasses', 1))  # Default to adding 1 glass
            WaterEntry.objects.create(user=request.user, glasses=glasses)
        return redirect('diary')  # Use 'diary' here instead of 'water_entry'


class SubtractWaterView(LoginRequiredMixin, View):
    login_url = '/login/'  # Set the login URL
    redirect_field_name = 'diary.html'

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            glasses = int(request.POST.get('glasses', 1))
            # Create a new WaterEntry to subtract the glasses

            WaterEntry.objects.create(user=request.user, glasses=-glasses)

        return redirect('diary')  # Redirect to the diary page
