import random
import weather_module
import news_module

import discord
from discord.ext import tasks, commands

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

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

# Отправка новостей
async def post_updates():
    channel = bot.get_channel(CHANNEL_ID)
    if channel:
        news_module.fetch_newsAPI(NEWS_API_KEY)

        #weather = weather_module.fetch_weather(WEATHER_API_KEY, WEATHER_CITY)
        await channel.send(f'Новости: {news_module.get_NewsUnit().title}')
        #await channel.send(f'Погода: {weather}')

#==========================TASKS_NEWS===========================

# Задача на отправку новостей (раз в час)
@tasks.loop(hours=1)
async def scheduled_task():
    await post_updates()

# Заявление о том что бот в системе
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    scheduled_task.start()

#==========================COMMANDS_NEWS===========================

#Команда приветсвия
@bot.command(name='hello')
async def hello(ctx):
    await ctx.send(f'Hello {ctx.author.mention}!')

#Команда отправки новости
@bot.command(name='more')
async def more(ctx):
    await ctx.send(f'Конечно, {ctx.author.mention}! Вот еще новости:')
    await post_updates()

@bot.command(name='debug')
async def debug(ctx):
    await ctx.send(f'Конечно, {ctx.author.mention}! Вот еще новости:')
    await post_updates()

# Запуск бота
init_config()
bot.run(DISCORD_TOKEN)