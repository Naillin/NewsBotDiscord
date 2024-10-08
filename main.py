import random
import weather_module
import news_module
import datetime
import asyncio

import discord
from discord.ext import tasks, commands

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# Начальная настройка бота и запуск конфига
def init_config():
    """
    Initializes the configuration by reading from the config.txt file.

    Sets the global variables:
        DISCORD_TOKEN
        CHANNEL_ID
        NEWS_API_KEY
        WEATHER_API_KEY
        WEATHER_CITY

    Returns:
        None
    """
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
async def post_news():
    try:
        channel = bot.get_channel(CHANNEL_ID)
        if channel:
            news_module.fetch_news_everything(NEWS_API_KEY) # добавить еще один api ключ от карпа как резерв. если израсходуется лимит первого начнет работать второй.

            news_unit = news_module.get_NewsUnit()
            if news_unit:
                embedNews = discord.Embed(
                    title=news_unit.title,
                    description=news_unit.description,
                    url=news_unit.url,
                    color=discord.Color.from_rgb(0, 255, 0)  # цвет embed
                )
                embedNews.set_author(name=news_unit.author)
                embedNews.set_image(url=news_unit.urlToImage)
                embedNews.add_field(
                    name="Статистика",
                    value=f"Количество запросов к API для текущей новости: {str(news_module.get_number_of_requests()[0])}.\n"
                          f"Всего запросов к API: {str(news_module.get_number_of_requests()[1])}.",
                    inline=False
                )
                await channel.send(embed=embedNews)
    except Exception as e:
        # Создаем embed-сообщение с ошибкой
        embedError = discord.Embed(title="Ошибка", color=discord.Color.from_rgb(255, 0, 0))
        embedError.add_field(name="Ошибка", value=str(e), inline=False)
        # Отправляем embed-сообщение в канал
        channel = bot.get_channel(CHANNEL_ID)
        await channel.send(embed=embedError)

async def post_weather():
    try:
        channel = bot.get_channel(CHANNEL_ID)
        if channel:
            weather_unit = weather_module.get_weather(WEATHER_API_KEY, WEATHER_CITY)

            if weather_unit:
                embedWeather = discord.Embed(
                    title=f"Погода в городе {WEATHER_CITY}",
                    color=discord.Color.from_rgb(0, 0, 255),
                    timestamp=datetime.datetime.now()
                )
                embedWeather.add_field(name="Описание", value=f"**{weather_unit.weather_description}**", inline=False)
                embedWeather.add_field(name="Температура(C)", value=f"**{weather_unit.temperature}°C**", inline=False)
                embedWeather.add_field(name="Влажность(%)", value=f"**{weather_unit.humidity}%**", inline=False)
                embedWeather.add_field(name="Атмосферное давление(hPa)", value=f"**{weather_unit.pressure}hPa**", inline=False)
                embedWeather.set_thumbnail(url="https://i.ibb.co/CMrsxdX/weather.png")
                embedWeather.set_footer(text=f"BlogDrone")
                await channel.send(embed=embedWeather)
    except Exception as e:
        # Создаем embed-сообщение с ошибкой
        embedError = discord.Embed(title="Ошибка", color=discord.Color.from_rgb(255, 0, 0))
        embedError.add_field(name="Ошибка", value=str(e), inline=False)
        # Отправляем embed-сообщение в канал
        channel = bot.get_channel(CHANNEL_ID)
        await channel.send(embed=embedError)
            
#==========================TASKS===========================

# Задача на отправку новостей (раз в 2 часа)
@tasks.loop(hours=2)
async def scheduled_task():
    await post_news()

    global __last_message
    __last_message = None
    loading_animation.restart()

# Задача на отправку погоды (раз в 8 часов)
@tasks.loop(hours=8)
async def post_weather_task():
    await post_weather()

    global __last_message
    __last_message = None
    loading_animation.restart()

__last_message = None
@tasks.loop(seconds=0.3)
async def loading_animation():
    global __last_message
    symbols = ['/', '-', '\\', '|']
    symbol = symbols[loading_animation.current_loop % len(symbols)]
    if __last_message is None:
        __last_message = await bot.get_channel(CHANNEL_ID).send(symbol)
    else:
        await __last_message.edit(content=symbol)

# Заявление о том что бот в системе
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    scheduled_task.start()
    post_weather_task.start()
    loading_animation.start()

#==========================COMMANDS===========================

#Команда приветсвия
@bot.command(name='hello')
async def hello(ctx):
    await ctx.send(f'Hello {ctx.author.mention}!')

    global __last_message
    __last_message = None
    loading_animation.restart()

#Команда отправки новости
@bot.command(name='more')
async def more(ctx):
    await ctx.send(f'Конечно, {ctx.author.mention}! Вот еще новости:')
    await post_news()
    await post_weather()

    global __last_message
    __last_message = None
    loading_animation.restart()

@bot.command(name='debug')
async def debug(ctx):
    await ctx.send(f"----------DEBUG----------")
    await ctx.send(f'Я BlogDrone. Состояние активен.')
    # Вывод информации о сервере
    await ctx.send(f"Сервер: {ctx.guild.name} (ID: {ctx.guild.id})")
    await ctx.send(f"Сервер создан: {ctx.guild.created_at}")
    await ctx.send(f"Сервер владелец: {ctx.guild.owner}")

    # Вывод информации о канале
    await ctx.send(f"Канал: {ctx.channel.name} (ID: {ctx.channel.id})")
    await ctx.send(f"Канал создан: {ctx.channel.created_at}")
    await ctx.send(f"Канал тип: {ctx.channel.type}")

    # Вывод информации о пользователе
    await ctx.send(f"Пользователь: {ctx.author.name} (ID: {ctx.author.id})")
    await ctx.send(f"Пользователь создан: {ctx.author.created_at}")
    await ctx.send(f"Пользователь статус: {ctx.author.status}")

    # Вывод информации о ролях пользователя
    await ctx.send(f"Роли пользователя: {[role.name for role in ctx.author.roles]}")

    # Вывод информации о разрешениях пользователя
    await ctx.send(f"Разрешения пользователя: {[perm[0] for perm in ctx.author.guild_permissions if perm[1]]}")

    # Вывод информации о сообщении
    await ctx.send(f"Сообщение: {ctx.message.content}")
    await ctx.send(f"Сообщение создан: {ctx.message.created_at}")
    await ctx.send(f"Сообщение тип: {ctx.message.type}")

    await ctx.send(f"----------Конец ответа----------")

    global __last_message
    __last_message = None
    loading_animation.restart()

@bot.command(name='rps')
async def rps(ctx):
    choices = ["камень", "ножницы", "бумага"]
    bot_choice = random.choice(choices)
    user_choice = ctx.message.content.split(" ")[1].lower() if len(ctx.message.content.split(" ")) > 1 else None
    if user_choice is None:
        await ctx.send("Неправильный выбор!")
    elif user_choice not in choices:
        await ctx.send("Неправильный выбор!")
    else:
        await ctx.send(f"Ваш выбор: {user_choice}, мой выбор: {bot_choice}.")
        if user_choice == bot_choice:
            await ctx.send("Ничья!")
        elif (user_choice == "камень" and bot_choice == "ножницы") or \
                (user_choice == "ножницы" and bot_choice == "бумага") or \
                (user_choice == "бумага" and bot_choice == "камень"):
            await ctx.send("Вы выиграли!")
        else:
            await ctx.send("Вы проиграли!")

    global __last_message
    __last_message = None
    loading_animation.restart()

@bot.command(name='helpp')
async def helpp(ctx):
    helpString = (
        f"Конечно, {ctx.author.mention}! Вот список команд:\n"
        f"!hello\n"
        f"!more\n"
        f"!rps\n"
        f"!debug\n"
    )
    await ctx.send(helpString)

    global __last_message
    __last_message = None
    loading_animation.restart()

#==========================START_BOT===========================

init_config()
bot.run(DISCORD_TOKEN)