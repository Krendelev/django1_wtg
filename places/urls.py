from django.urls import path

from .views import get_places, get_place_details

urlpatterns = [
    path("", get_places, name="places"),
    path("places/<int:pk>", get_place_details, name="place-details"),
]
