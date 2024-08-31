from django.urls import path

from . import views
from .views import DiaryView, AddWaterView, SubtractWaterView

# url patterns are created in here

urlpatterns = [

    path("", DiaryView.as_view(), name="diary"),
    path('add_water/', AddWaterView.as_view(), name='add_water'),
    path('subtract_water/', SubtractWaterView.as_view(), name='subtract_water'),

]
