import discord
import requests
import schedule
import time
from discord.ext import tasks

# meta infa переместить в файл констант
DISCORD_TOKEN = 'YOUR_DISCORD_BOT_TOKEN'
NEWS_API_KEY = 'YOUR_NEWS_API_KEY'
WEATHER_API_KEY = 'YOUR_WEATHER_API_KEY'
CHANNEL_ID = YOUR_CHANNEL_ID  # ID канала, куда бот будет отправлять сообщения
# meta infa переместить в файл констант

client = discord.Client()

def fetch_news():
    url = f'https://newsapi.org/v2/top-headlines?country=us&apiKey={NEWS_API_KEY}'
    response = requests.get(url)
    data = response.json()
    articles = data.get('articles', [])
    if articles:
        return articles[0]['title']  # Возвращаем заголовок первой статьи
    return 'Нет доступных новостей.'

def fetch_weather():
    city = 'YOUR_CITY'
    url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric'
    response = requests.get(url)
    data = response.json()
    weather_description = data['weather'][0]['description']
    temperature = data['main']['temp']
    return f'Погода в {city}: {weather_description}, {temperature}°C'

async def post_updates():
    channel = client.get_channel(CHANNEL_ID)
    if channel:
        news = fetch_news()
        weather = fetch_weather()
        await channel.send(f'Новости: {news}')
        await channel.send(f'Погода: {weather}')

@tasks.loop(hours=1)
async def scheduled_task():
    await post_updates()

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')
    scheduled_task.start()

client.run(DISCORD_TOKEN)
