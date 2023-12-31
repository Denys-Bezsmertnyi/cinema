# Generated by Django 5.0 on 2023-12-07 14:31

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CinemaHall',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('places', models.PositiveIntegerField(default=1)),
            ],
        ),
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('image', models.ImageField(default='static/img/movie_default.jpg', upload_to='movie_images/')),
            ],
        ),
        migrations.CreateModel(
            name='MovieSession',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('time_start', models.TimeField()),
                ('time_end', models.TimeField()),
                ('date_start', models.DateField()),
                ('date_end', models.DateField()),
                ('hall', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sessions', to='cinema.cinemahall')),
                ('movie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cinema.movie')),
            ],
        ),
    ]
