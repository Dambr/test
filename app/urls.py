from django.urls import path
from .views import ReviewView
app_name = "reviews"
# app_name will help us do a reverse look-up latter.
urlpatterns = [
    path('', ReviewView.as_view()),
]