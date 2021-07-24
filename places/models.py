from django.db import models
from tinymce.models import HTMLField


class Place(models.Model):
    title = models.CharField(max_length=100, verbose_name="Название")
    short_description = models.TextField(blank=True, verbose_name="Синопсис")
    long_description = HTMLField(blank=True, verbose_name="Описание")
    longitude = models.FloatField(verbose_name="Долгота")
    latitude = models.FloatField(verbose_name="Широта")

    class Meta:
        verbose_name = "Место"
        verbose_name_plural = "Места"

    def __str__(self):
        return self.title


def photo_directory_path(instance, filename):
    return f"{instance.place.id}/{filename}"


class Photo(models.Model):
    place = models.ForeignKey(
        Place,
        on_delete=models.CASCADE,
        related_name="photos",
        verbose_name="Место",
    )
    position = models.PositiveSmallIntegerField(default=0, verbose_name="Позиция")
    photo = models.ImageField(upload_to=photo_directory_path, verbose_name="Фото")

    class Meta:
        verbose_name = "Фото"
        verbose_name_plural = "Фото"
        ordering = ["position"]

    def __str__(self):
        return f"{self.position} {self.place.title}"
