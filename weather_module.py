import requests
# Получение погоды
def fetch_weather(WEATHER_API_KEY, WEATHER_CITY):
    url = f'https://api.openweathermap.org/data/2.5/weather?q={WEATHER_CITY}&appid={WEATHER_API_KEY}&units=metric'
    response = requests.get(url)
    data = response.json()
    weather_description = data['weather'][0]['description']
    temperature = data['main']['temp']
    return f'Погода в {WEATHER_CITY}: {weather_description}, {temperature}°C'

