# Generated by Django 2.0.2 on 2018-04-18 20:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('www', '0014_weather_weather_icon'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='weather',
            name='weather_icon',
        ),
        migrations.AddField(
            model_name='weather',
            name='weather_day',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='weather_day', to='www.WeatherIcon'),
        ),
        migrations.AddField(
            model_name='weather',
            name='weather_night',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='weather_night', to='www.WeatherIcon'),
        ),
    ]
