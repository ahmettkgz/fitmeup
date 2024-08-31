from django.urls import path, include
from .views import RegisterView, LoginUserView, LogoutUserView, ProfileView, ProfileUpdateView

# url patterns are created in here

# the as_view() method is called to convert the MyView class into a callable view.
urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path('login/', LoginUserView.as_view(), name='login'),
    path('logout/', LogoutUserView.as_view(), name='logout'),
    path("", ProfileView.as_view(), name="mainpage"),
    path("<int:pk>/update/", ProfileUpdateView.as_view(), name="profileupdate"),
    path("", include('django.contrib.auth.urls'))  # use djangos authentication system instead of creating a new system
]
