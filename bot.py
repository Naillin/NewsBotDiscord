import discord
import requests
import schedule
import time
from discord.ext import tasks

client = discord.Client()

# Начальная настройка бота и запуск конфига
def init_config():
    global DISCORD_TOKEN, CHANNEL_ID, NEWS_API_KEY, WEATHER_API_KEY, WEATHER_CITY
    # Открываем файл для чтения
    with open('config.txt', 'r', encoding='utf-8') as file:
        config = {}
        for line in file:
            # Удаляем лишние пробелы и символы новой строки
            line = line.strip()
            if line and '=' in line:  # Проверяем, что строка не пустая и содержит '='
                key, value = line.split('=', 1)  # Разделяем строку по первому вхождению '='
                config[key.strip()] = value.strip()  # Сохраняем в словарь, убирая лишние пробелы

    DISCORD_TOKEN = config['DISCORD_TOKEN']
    CHANNEL_ID = int(config['CHANNEL_ID'])
    NEWS_API_KEY = config['NEWS_API_KEY']
    WEATHER_API_KEY = config['WEATHER_API_KEY']
    WEATHER_CITY = config['WEATHER_CITY']

# Получение новостей
def fetch_news():
    url = f'https://newsapi.org/v2/top-headlines?country=us&apiKey={NEWS_API_KEY}'
    response = requests.get(url)
    data = response.json()
    articles = data.get('articles', [])
    if articles:
        return articles[0]['title']  # Возвращаем заголовок первой статьи
    return 'Нет доступных новостей.'

# Получение погоды
def fetch_weather():
    url = f'https://api.openweathermap.org/data/2.5/weather?q={WEATHER_CITY}&appid={WEATHER_API_KEY}&units=metric'
    response = requests.get(url)
    data = response.json()
    weather_description = data['weather'][0]['description']
    temperature = data['main']['temp']
    return f'Погода в {WEATHER_CITY}: {weather_description}, {temperature}°C'

# Отправка новостей
async def post_updates():
    channel = client.get_channel(CHANNEL_ID)
    if channel:
        news = fetch_news()
        weather = fetch_weather()
        await channel.send(f'Новости: {news}')
        await channel.send(f'Погода: {weather}')

# Задача на отправку новостей (раз в час)
@tasks.loop(hours=1)
async def scheduled_task():
    await post_updates()

# Заявление о том что бот в системе
@client.event
async def on_ready():
    print(f'Logged in as {client.user}')
    scheduled_task.start()

# Запуск бота
init_config()
client.run(DISCORD_TOKEN)
