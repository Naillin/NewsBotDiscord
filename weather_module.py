import requests
from weather_unit import WeatherUnit
from requests.adapters import HTTPAdapter
from requests.exceptions import ConnectionError


# Получение погоды
def get_weather(WEATHER_API_KEY, WEATHER_CITY: str):
    url = f'https://api.openweathermap.org/data/2.5/weather?q={WEATHER_CITY}&appid={WEATHER_API_KEY}&units=metric'

    #  адаптер для HTTP-запросов, который позволяет повторять запросы в случае неудачи(5 раз).
    WeatherAdapter = HTTPAdapter(max_retries=20)
    session = requests.Session()
    session.mount('https://api.openweathermap.org', WeatherAdapter)

    response = session.get(url)  # Используйте сессию для отправки запроса
    data = response.json()


    y=data["main"]
    current_temperature = round(y["temp"], 1)
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


