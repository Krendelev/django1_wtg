from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from .models import Place


def serialize_places(places):
    serialized_places = {
        "places": {
            "type": "FeatureCollection",
            "features": [
                {
                    "type": "Feature",
                    "geometry": {
                        "type": "Point",
                        "coordinates": [place.longitude, place.latitude],
                    },
                    "properties": {
                        "title": place.title,
                        "placeId": place.id,
                        "detailsUrl": reverse("place-details", args=[place.id]),
                    },
                }
                for place in places
            ],
        }
    }
    return serialized_places


def get_places(request):
    places = Place.objects.all()
    context = serialize_places(places)
    return render(request, "index.html", context=context)


def get_place_details(request, pk):
    place = get_object_or_404(Place, pk=pk)
    context = {
        "title": place.title,
        "imgs": [obj.photo.url for obj in place.photos.all()],
        "description_short": place.short_description,
        "description_long": place.long_description,
        "coordinates": {"lat": place.latitude, "lng": place.longitude},
    }
    return JsonResponse(context, json_dumps_params={"ensure_ascii": False, "indent": 2})
