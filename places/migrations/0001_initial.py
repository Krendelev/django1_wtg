# Generated by Django 3.2.5 on 2021-07-23 01:23

from django.db import migrations, models
import django.db.models.deletion
import places.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Place',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='Название')),
                ('short_description', models.TextField(blank=True, verbose_name='Синопсис')),
                ('long_description', models.TextField(blank=True, verbose_name='Описание')),
                ('longitude', models.FloatField(verbose_name='Долгота')),
                ('latitude', models.FloatField(verbose_name='Широта')),
            ],
            options={
                'verbose_name': 'Место',
                'verbose_name_plural': 'Места',
            },
        ),
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position', models.PositiveSmallIntegerField(default=0, verbose_name='Позиция')),
                ('photo', models.ImageField(upload_to=places.models.photo_directory_path, verbose_name='Фото')),
                ('place', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='photos', to='places.place', verbose_name='Место')),
            ],
            options={
                'verbose_name': 'Фото',
                'verbose_name_plural': 'Фото',
                'ordering': ['position'],
            },
        ),
    ]
