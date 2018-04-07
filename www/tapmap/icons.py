from .locations import LOCATIONS
from www.taps.forecast import query
from .codetoicon import GetClothingIcon, GetWeatherIcon

I_WIDTH  = 100
I_HEIGHT = 100
C_WIDTH = 1164
C_HEIGHT = 1530


def get_weather():
    icons = list()

    for location in LOCATIONS:
        weather = query(location["name"])
        forecast = GetWeatherIcon(weather["code"], weather["daytime"])
        icons.append({
            "src": "map/weather/" + forecast + ".svg",
            "scale": 0.15,
            "x": round((location["x"]*C_WIDTH) - (I_WIDTH/2)),
            "y": round((location["y"]*C_HEIGHT) - (I_HEIGHT/2))
        })
    
    return icons
        

def get_clothing():
    icons = list()

    for location in LOCATIONS:
        weather = query(location["name"])

        if (weather["taps"]["status"]=="aff"):
            clothing="tapsaff"
        else:
            clothing = GetClothingIcon(weather["code"], weather["temp_c"])

        icons.append({
            "src": "map/clothing/" + clothing + ".svg",
            "scale": 0.1,
            "x": round((location["x"]*C_WIDTH) - (I_WIDTH/2)),
            "y": round((location["y"]*C_HEIGHT) - (I_HEIGHT/2))
        })
    
    return icons