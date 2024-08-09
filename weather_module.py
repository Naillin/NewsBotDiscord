import requests
from weather_unit import WeatherUnit

# Получение погоды
def get_weather(WEATHER_API_KEY, WEATHER_CITY: str):
    url = f'https://api.openweathermap.org/data/2.5/weather?q={WEATHER_CITY}&appid={WEATHER_API_KEY}&units=metric'
    response = requests.get(url)
    data = response.json()

    y=data["main"]
    current_temperature = y["Температура"]
    current_temperature_celsiuis = str(round(current_temperature - 273.15))
    current_pressure = y["Давление"]
    current_humidity = y["Влажность"]
    z=data["Погода"]

    weather_description = z[0]["Описание"]

    return WeatherUnit(
        weather_description,
        current_temperature_celsiuis,
        current_humidity,
        current_pressure
    )


