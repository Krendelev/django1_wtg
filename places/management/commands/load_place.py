from pathlib import Path

import requests
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from places.models import Photo, Place


class Command(BaseCommand):
    help = "Добавляет объект в базу данных"

    def add_arguments(self, parser):
        parser.add_argument("url")

    def handle(self, *args, **options):
        response = requests.get(options["url"], timeout=5)
        response.raise_for_status()
        place_info = response.json()

        place, created = Place.objects.get_or_create(
            title=place_info["title"],
            defaults={
                "short_description": place_info["description_short"],
                "long_description": place_info["description_long"],
                "longitude": place_info["coordinates"]["lng"],
                "latitude": place_info["coordinates"]["lat"],
            },
        )

        missed_images = []
        for index, url in enumerate(place_info["imgs"], start=1):
            image, created = Photo.objects.get_or_create(place=place, position=index)
            image_name = Path(url).name
            try:
                response = requests.get(url, timeout=5)
                response.raise_for_status()
            except (requests.HTTPError, requests.ConnectionError) as err:
                missed_images.append(image_name)

            image.photo.save(image_name, ContentFile(response.content), save=True)

        if missed_images:
            self.stderr.write(
                self.style.WARNING(f"Не удалось загрузить: {missed_images}")
            )

        self.stdout.write(
            self.style.SUCCESS(f"Объект {place_info['title']} успешно добавлен в базу")
        )
