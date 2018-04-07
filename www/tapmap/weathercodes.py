TEMPERATURES = [
  {"title": "colder", "lowerBound": -273.15},
  {"title": "cold",   "lowerBound":       5},
  {"title": "fair",   "lowerBound":      11},
  {"title": "warm",   "lowerBound":      16}
]

WEATHER_CLOTHING = [
  {"colder": "jacket", "cold": "jacket", "fair": "jacket", "warm": "hoodie"}, # 00 - tornado
  {"colder": "jacket", "cold": "jacket", "fair": "jacket", "warm": "hoodie"}, # 01 - tropical storm
  {"colder": "jacket", "cold": "jacket", "fair": "jacket", "warm": "hoodie"}, # 02 - hurricane
  {"colder": "jacket", "cold": "jacket", "fair": "jacket", "warm": "hoodie"}, # 03 - severe thunderstorms
  {"colder": "jacket", "cold": "jacket", "fair": "jacket", "warm": "hoodie"}, # 04 - thunderstorms
  {"colder": "jacket", "cold": "jacket", "fair": "jacket", "warm": "hoodie"}, # 05 - mixed rain and snow
  {"colder": "jacket", "cold": "jacket", "fair": "jacket", "warm": "hoodie"}, # 06 - mixed rain and sleet
  {"colder": "jacket", "cold": "jacket", "fair": "jacket", "warm": "hoodie"}, # 07 - mixed snow and sleet
  {"colder": "jacket", "cold": "jacket", "fair": "jacket", "warm": "hoodie"}, # 08 - freezing drizzle
  {"colder": "jacket", "cold": "jacket", "fair": "jacket", "warm": "hoodie"}, # 09 - drizzle
  {"colder": "jacket", "cold": "jacket", "fair": "jacket", "warm": "hoodie"}, # 10 - freezing rain
  {"colder": "jacket", "cold": "jacket", "fair": "jacket", "warm": "hoodie"}, # 11 - showers
  {"colder": "jacket", "cold": "jacket", "fair": "jacket", "warm": "hoodie"}, # 12 - showers
  {"colder": "jacket", "cold": "jacket", "fair": "jacket", "warm": "hoodie"}, # 13 - snow flurries
  {"colder": "jacket", "cold": "jacket", "fair": "jacket", "warm": "hoodie"}, # 14 - light snow showers
  {"colder": "jacket", "cold": "jacket", "fair": "jacket", "warm": "hoodie"}, # 15 - blowing snow
  {"colder": "jacket", "cold": "jacket", "fair": "jacket", "warm": "hoodie"}, # 16 - snow
  {"colder": "jacket", "cold": "jacket", "fair": "jacket", "warm": "hoodie"}, # 17 - hail
  {"colder": "jacket", "cold": "jacket", "fair": "jacket", "warm": "hoodie"}, # 18 - sleet
  {"colder": "jacket", "cold": "jacket", "fair": "tshirt", "warm": "tshirt"}, # 19 - dust
  {"colder": "jacket", "cold": "hoodie", "fair": "tshirt", "warm": "tshirt"}, # 20 - foggy
  {"colder": "jacket", "cold": "hoodie", "fair": "tshirt", "warm": "tshirt"}, # 21 - haze
  {"colder": "jacket", "cold": "hoodie", "fair": "tshirt", "warm": "tshirt"}, # 22 - smoky
  {"colder": "jacket", "cold": "jacket", "fair": "hoodie", "warm": "tshirt"}, # 23 - blustery
  {"colder": "jacket", "cold": "jacket", "fair": "hoddie", "warm": "tshirt"}, # 24 - windy
  {"colder": "jacket", "cold": "jacket", "fair": "hoodie", "warm": "hoodie"}, # 25 - cold
  {"colder": "jacket", "cold": "hoodie", "fair": "tshirt", "warm": "tshirt"}, # 26 - cloudy
  {"colder": "jacket", "cold": "hoodie", "fair": "hoodie", "warm": "tshirt"}, # 27 - mostly cloudy (night)
  {"colder": "jacket", "cold": "hoodie", "fair": "tshirt", "warm": "tshirt"}, # 28 - mostly cloudy (day)
  {"colder": "jacket", "cold": "hoodie", "fair": "hoodie", "warm": "tshirt"}, # 29 - partly cloudy (night)
  {"colder": "jacket", "cold": "hoodie", "fair": "tshirt", "warm": "tshirt"}, # 30 - partly cloudy (day)
  {"colder": "jacket", "cold": "hoodie", "fair": "hoodie", "warm": "tshirt"}, # 31 - clear (night)
  {"colder": "jacket", "cold": "hoodie", "fair": "tshirt", "warm": "tshirt"}, # 32 - sunny
  {"colder": "jacket", "cold": "hoodie", "fair": "tshirt", "warm": "tshirt"}, # 33 - fair (night)
  {"colder": "jacket", "cold": "hoodie", "fair": "tshirt", "warm": "tshirt"}, # 34 - fair (day)
  {"colder": "jacket", "cold": "jacket", "fair": "jacket", "warm": "hoodie"}, # 35 - mixed rain and hail
  {"colder": "jacket", "cold": "hoodie", "fair": "hoodie", "warm": "tshirt"}, # 36 - hot
  {"colder": "jacket", "cold": "jacket", "fair": "hoodie", "warm": "tshirt"}, # 37 - isolated thunderstorms
  {"colder": "jacket", "cold": "jacket", "fair": "hoodie", "warm": "tshirt"}, # 38 - scattered thunderstorms
  {"colder": "jacket", "cold": "jacket", "fair": "hoodie", "warm": "tshirt"}, # 39 - scattered showers
  {"colder": "jacket", "cold": "jacket", "fair": "hoodie", "warm": "tshirt"}, # 40 - scattered showers
  {"colder": "jacket", "cold": "jacket", "fair": "jacket", "warm": "hoodie"}, # 41 - heavy snow
  {"colder": "jacket", "cold": "jacket", "fair": "jacket", "warm": "hoodie"}, # 42 - scattered snow showers
  {"colder": "jacket", "cold": "jacket", "fair": "jacket", "warm": "hoodie"}, # 43 - heavy snow
  {"colder": "jacket", "cold": "hoodie", "fair": "hoodie", "warm": "tshirt"}, # 44 - partly cloudy
  {"colder": "jacket", "cold": "jacket", "fair": "jacket", "warm": "tshirt"}, # 45 - thundershowers
  {"colder": "jacket", "cold": "jacket", "fair": "jacket", "warm": "hoodie"}, # 46 - snow showers
  {"colder": "jacket", "cold": "jacket", "fair": "jacket", "warm": "tshirt"}  # 47 - isolated thundershowers
]

WEATHER_ICON = [
  {"day": "wind_lightning",   "night": "wind_lightning"},   # 00 - tornado
  {"day": "wind_rain",        "night": "wind_rain"},        # 01 - tropical storm
  {"day": "windy",            "night": "cloud_wind_night"}, # 02 - hurricane
  {"day": "wind_lightning",   "night": "wind_lightning"},   # 03 - severe thunderstorms
  {"day": "wind_lightning",   "night": "wind_lightning"},   # 04 - thunderstorms
  {"day": "rain_snow",        "night": "rain_snow"},        # 05 - mixed rain and snow
  {"day": "rain_snow",        "night": "rain_snow"},        # 06 - mixed rain and sleet
  {"day": "rain_snow",        "night": "rain_snow"},        # 07 - mixed snow and sleet
  {"day": "drizzle",          "night": "cloud_rain_night"}, # 08 - freezing drizzle
  {"day": "rain",             "night": "cloud_rain_night"}, # 09 - drizzle
  {"day": "drizzle",          "night": "cloud_rain_night"}, # 10 - freezing rain
  {"day": "showers",          "night": "showers"},          # 11 - showers
  {"day": "showers",          "night": "showers"},          # 12 - showers
  {"day": "wind_cloud_snow",  "night": "snow_night"},       # 13 - snow flurries
  {"day": "wind_cloud_snow",  "night": "snow_night"},       # 14 - light snow showers
  {"day": "wind_cloud_snow",  "night": "snow_night"},       # 15 - blowing snow
  {"day": "cloud_snow",       "night": "snow_night"},       # 16 - snow
  {"day": "rain_snow",        "night": "rain_snow"},        # 17 - hail
  {"day": "rain_snow",        "night": "rain_snow"},        # 18 - sleet
  {"day": "windy",            "night": "windy"},            # 19 - dust
  {"day": "fog",              "night": "fog"},              # 20 - foggy
  {"day": "fog",              "night": "fog"},              # 21 - haze
  {"day": "fog",              "night": "fog"},              # 22 - smoky
  {"day": "windy",            "night": "windy"},            # 23 - blustery
  {"day": "windy",            "night": "windy"},            # 24 - windy
  {"day": "temp_low",         "night": "temp_low"},         # 25 - cold
  {"day": "cloud",            "night": "cloud_night"},      # 26 - cloudy
  {"day": "cloud_night",      "night": "cloud_night"},      # 27 - mostly cloudy (night)
  {"day": "cloud_sun",        "night": "cloud_night"},      # 28 - mostly cloudy (day)
  {"day": "cloud_night",      "night": "cloud_night"},      # 29 - partly cloudy (night)
  {"day": "cloud_sun",        "night": "cloud_night"},      # 30 - partly cloudy (day)
  {"day": "clear_night",      "night": "clear_night"},      # 31 - clear (night)
  {"day": "sun_clear",        "night": "clear_night"},      # 32 - sunny
  {"day": "clear_night",      "night": "clear_night"},      # 33 - fair (night)
  {"day": "sun_clear",        "night": "clear_night"},      # 34 - fair (day)
  {"day": "rain_snow",        "night": "rain_snow"},        # 35 - mixed rain and hail
  {"day": "temp_high",        "night": "temp_high"},        # 36 - hot
  {"day": "lightning",        "night": "lightning_night"},  # 37 - isolated thunderstorms
  {"day": "lightning",        "night": "lightning_night"},  # 38 - scattered thunderstorms
  {"day": "showers",          "night": "showers"},          # 39 - scattered showers
  {"day": "showers",          "night": "showers"},          # 40 - scattered showers
  {"day": "cloud_snow",       "night": "snow_night"},       # 41 - heavy snow
  {"day": "cloud_snow",       "night": "snow_night"},       # 42 - scattered snow showers
  {"day": "cloud_snow",       "night": "snow_night"},       # 43 - heavy snow
  {"day": "cloud",            "night": "cloud_night"},      # 44 - partly cloudy
  {"day": "rain_lightning",   "night": "rain_lightning"},   # 45 - thundershowers
  {"day": "rain_snow",        "night": "rain_snow"},        # 46 - snow showers
  {"day": "rain_lightning",   "night": "rain_lightning"}    # 47 - isolated thundershowers
]
