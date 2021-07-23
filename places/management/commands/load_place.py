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
        raw_place = response.json()

        place, created = Place.objects.get_or_create(
            title=raw_place["title"],
            defaults={
                "short_description": raw_place["description_short"],
                "long_description": raw_place["description_long"],
                "longitude": raw_place["coordinates"]["lng"],
                "latitude": raw_place["coordinates"]["lat"],
            },
        )

        missed_images = []
        for index, url in enumerate(raw_place["imgs"], start=1):
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
            self.style.SUCCESS(f"Объект {raw_place['title']} успешно добавлен в базу")
        )
