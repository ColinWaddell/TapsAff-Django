# System
import csv
import sys

# Django
from sys import stdin, stdout
from django.core.management.base import BaseCommand
from argparse import FileType

# Models
from www.models import Weather, ClothingIcon, WeatherIcon

# Rows
CODE = 0
DAY = 1
SCOTS = 2
TERRIBLE = 3
DELTA = 4
COLDER = 5
COLD = 6
FAIR = 7
WARM = 8
CLOTHING_COLDER = 9
CLOTHING_COLD = 10
CLOTHING_FAIR = 11
CLOTHING_WARM = 12
WEATHER_DAY = 13
WEATHER_NIGHT = 14


class Command(BaseCommand):
    help = "Import weather codes as CSV"

    def add_arguments(self, parser):
        parser.add_argument("csv_path", nargs=1, type=FileType("r"), default=stdin)

    def valid_headers(self, row):
        return (
            row[CODE] == "code"
            and row[DAY] == "day"
            and row[SCOTS] == "Scots"
            and row[TERRIBLE] == "Terrible"
            and row[DELTA] == "Delta"
            and row[COLDER] == "Colder"
            and row[COLD] == "Cold"
            and row[FAIR] == "Fair"
            and row[WARM] == "Warm"
            and row[CLOTHING_COLDER] == "Clothing Colder"
            and row[CLOTHING_COLD] == "Clothing Cold"
            and row[CLOTHING_FAIR] == "Clothing Fair"
            and row[CLOTHING_WARM] == "Clothing Warm"
            and row[WEATHER_DAY] == "Weather Day"
            and row[WEATHER_NIGHT] == "Weather Night"
        )

    def handle(self, *args, **options):
        input_csv = options["csv_path"][0].name

        with open(input_csv, newline="") as csvfile:
            reader = csv.reader(csvfile, delimiter=",")
            first_row = True
            for row in reader:
                # Check for valid data
                if first_row:
                    first_row = False
                    if not self.valid_headers(row):
                        print("Error: CSV Columns Invalid")
                        sys.exit()
                    continue

                # Look up fks
                clothing_colder = ClothingIcon.objects.get(icon=row[CLOTHING_COLDER])
                clothing_cold = ClothingIcon.objects.get(icon=row[CLOTHING_COLD])
                clothing_fair = ClothingIcon.objects.get(icon=row[CLOTHING_FAIR])
                clothing_warm = ClothingIcon.objects.get(icon=row[CLOTHING_WARM])
                weather_day = WeatherIcon.objects.get(icon=row[WEATHER_DAY])
                weather_night = WeatherIcon.objects.get(icon=row[WEATHER_NIGHT])

                # Create model
                weather = Weather(
                    code=row[CODE],
                    description=row[DAY],
                    scots=row[SCOTS],
                    terrible=row[TERRIBLE],
                    delta=row[DELTA],
                    colder=row[COLDER],
                    cold=row[COLD],
                    fair=row[FAIR],
                    warm=row[WARM],
                    clothing_colder=clothing_colder,
                    clothing_cold=clothing_cold,
                    clothing_fair=clothing_fair,
                    clothing_warm=clothing_warm,
                    weather_day=weather_day,
                    weather_night=weather_night,
                )
                weather.save()
                print(f"{row[0]} ({row[1]}) added to database")
