from adminsortable2.admin import SortableInlineAdminMixin
from django.contrib import admin
from django.utils.html import format_html

from .models import Photo, Place


class PhotoInline(SortableInlineAdminMixin, admin.TabularInline):
    model = Photo
    extra = 1
    fields = ["photo", "thumbnail"]
    readonly_fields = ["thumbnail"]

    def thumbnail(self, obj):
        return (
            format_html("<img src='{}' height='200' />", obj.photo.url)
            if obj.photo
            else "Фото ещё не загружено"
        )


@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
    inlines = [PhotoInline]
    search_fields = ["title"]
