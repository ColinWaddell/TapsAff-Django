# Generated by Django 2.0.2 on 2018-04-18 21:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('www', '0015_auto_20180418_2056'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='settings',
            name='cold',
        ),
        migrations.RemoveField(
            model_name='settings',
            name='colder',
        ),
        migrations.RemoveField(
            model_name='settings',
            name='fair',
        ),
        migrations.RemoveField(
            model_name='settings',
            name='warm',
        ),
        migrations.AddField(
            model_name='weather',
            name='cold',
            field=models.FloatField(default=5),
        ),
        migrations.AddField(
            model_name='weather',
            name='colder',
            field=models.FloatField(default=-273.15),
        ),
        migrations.AddField(
            model_name='weather',
            name='fair',
            field=models.FloatField(default=13),
        ),
        migrations.AddField(
            model_name='weather',
            name='warm',
            field=models.FloatField(default=16),
        ),
    ]
