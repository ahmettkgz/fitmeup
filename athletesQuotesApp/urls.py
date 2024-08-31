from django.urls import path
from .views import AthletesQuotesView, AthleteQuoteCreateView, AthleteQuoteUpdateView, AthleteQuoteDeleteView, \
    AthleteQuoteDetailsView

#url patterns are created in here

#he as_view() method is called to convert the MyView class into a callable view.
urlpatterns = [
 #   path("", IndexView.as_view(), name="index"),
    path("", AthletesQuotesView.as_view(), name="athletesquotes"),
    path("new/", AthleteQuoteCreateView.as_view(), name="quote_create"),
    path("<int:pk>/update/", AthleteQuoteUpdateView.as_view(), name="quote_update"),
    # primary key is necessary for the specific blog
    path("<int:id>", AthleteQuoteDetailsView.as_view(), name="quote_details"),
    path("<int:pk>/delete/", AthleteQuoteDeleteView.as_view(), name="quote_delete")
 ]