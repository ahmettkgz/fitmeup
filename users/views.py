from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.generic import View, UpdateView
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from users.forms import RegisterUserForm, ProfileUpdateForm
from users.models import Chef, Other, Athlete
from common.models import BasePerson
from django.contrib.auth.models import User


class RegisterView(View):
    def get(self, request):
        # Display the registration form
        form = RegisterUserForm()

        return render(request, 'users/register.html', {'form': form})

    def post(self, request):
        form = RegisterUserForm(request.POST)

        if form.is_valid():

            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            date_of_birth = None
            gender = None
            height = None
            exercise_per_week = None
            weight = None
            purpose = 'lose_weight'

            user = authenticate(username=username, password=password)
            login(request, user)

            if form.cleaned_data['occupation'] == 'athlete':
                # Create an Athlete object and link it to the user
                sport = None
                athlete_profile = Athlete.objects.create(
                    user=user,
                    occupation='athlete',
                    date_of_birth=date_of_birth,
                    gender=gender,
                    height=height,
                    weight=weight,
                    exercise_per_week=exercise_per_week,
                    purpose=purpose,
                    sport=sport
                )
                athlete_profile.save()
            elif form.cleaned_data['occupation'] == 'chef':

                chef_profile = Chef.objects.create(user=user,
                                                   occupation='chef',
                                                   date_of_birth=date_of_birth,
                                                   gender=gender,
                                                   height=height,
                                                   weight=weight,
                                                   exercise_per_week=exercise_per_week,
                                                   purpose=purpose
                                                   )
                chef_profile.save()
            elif form.cleaned_data['occupation'] == 'other':

                other_profile = Other.objects.create(user=user,
                                                     occupation='other',
                                                     date_of_birth=date_of_birth,
                                                     gender=gender,
                                                     height=height,
                                                     weight=weight,
                                                     exercise_per_week=exercise_per_week,
                                                     purpose=purpose
                                                     )
                other_profile.save()

            return redirect('index')

        return render(request, 'users/register.html', {'form': form})


class LoginUserView(View):

    def get(self, request):
        return render(request, 'users/login.html', {})

    def post(self, request):
        if request.method == "POST":

            username = request.POST.get("username", "")
            password = request.POST.get("password", "")
            # Authenticate user credentials
            user = authenticate(request, username=username, password=password)

            if user is not None:

                login(request, user)
                return redirect('mainpage')
            else:

                messages.success(request, "There was an error  Logging In, Please try again..")
                return redirect('login')


class LogoutUserView(View):
    def get(self, request):
        return render(request, 'users/logoutconfirm.html')

    def post(self, request):
        # Perform the logout when the confirmation form is submitted
        logout(request)
        messages.success(request, "You were logged out.")
        return redirect('index')


class ProfileView(View):

    def get(self, request): 
        for my_class in [Athlete, Chef, Other]:
            try:
                myperson = my_class.objects.get(user=request.user)
                context = {"myperson": myperson}
                break
            except:
                myperson = None
        if myperson is None:
            context = {"myperson": myperson}

        return render(request, "mainpage.html", context=context)


class ProfileUpdateView(LoginRequiredMixin, UserPassesTestMixin, View):
    template_name = 'users/profileupdate.html'
    form_class = ProfileUpdateForm

    def test_func(self):
        user_profile = self.get_user_profile(self.request.user)
        if user_profile:
            return True if user_profile.user == self.request.user else False
        return False

    def get_user_profile(self, user):
        user_profiles = [Athlete, Chef, Other]
        for profile_model in user_profiles:
            try:
                return profile_model.objects.get(user=user)
            except profile_model.DoesNotExist:
                pass
        return None

    def get(self, request, pk):
        user_profile = self.get_user_profile(request.user)
        if user_profile:
            initial_data = {field.name: getattr(user_profile, field.name) for field in user_profile._meta.fields}
            form = self.form_class(instance=user_profile, initial=initial_data)
        else:
            form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, pk):
        user_profile = self.get_user_profile(request.user)
        form = self.form_class(request.POST, instance=user_profile)
        if form.is_valid():
            user_profile = form.save(commit=False)
            user_profile.user = request.user  # Set the user field
            user_profile.save()
            messages.success(request, 'Your profile is updated successfully')
            return redirect('mainpage')

        return render(request, self.template_name, {'form': form})


