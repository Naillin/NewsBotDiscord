import requests
from weather_unit import WeatherUnit

# Получение погоды
def get_weather(WEATHER_API_KEY, WEATHER_CITY: str):
    url = f'https://api.openweathermap.org/data/2.5/weather?q={WEATHER_CITY}&appid={WEATHER_API_KEY}&units=metric'
    response = requests.get(url)
    data = response.json()

    y=data["main"]
    current_temperature = y["temp"]
    current_pressure = y["pressure"]
    current_humidity = y["humidity"]
    z=data["weather"]

    weather_description = z[0]["description"]

    return WeatherUnit(
        weather_description,
        current_temperature,
        current_humidity,
        current_pressure
    )


