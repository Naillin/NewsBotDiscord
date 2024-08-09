import requests
import discord

from discord import Embed
# Получение погоды
async def weather(ctx, WEATHER_API_KEY, *, WEATHER_CITY: str):
    url = f'https://api.openweathermap.org/data/2.5/weather?q={WEATHER_CITY}&appid={WEATHER_API_KEY}&units=metric'
    response = requests.get(url)
    data = response.json()
    channel = ctx.message.channel

    y=data["main"]
    current_temperature = y["Температура"]
    current_temperature_celsiuis = str(round(current_temperature - 273.15))
    current_pressure = y["Давление"]
    current_humidity = y["Влажность"]
    z=data["Погода"]

    weather_description = z[0]["Описание"]
    embed = discord.Embed(
        title=f"Погода в городе {WEATHER_CITY}", color=ctx.guild.me.top_role.color, timestamp=ctx.message.created_at,)
    embed.add_field(name="Описание", value=f"**{weather_description}**", inline=False)
    embed.add_field(name="Температура(C)", value=f"**{current_temperature_celsiuis}°C**", inline=False)
    embed.add_field(name="Влажность(%)", value=f"**{current_humidity}%**", inline=False)
    embed.add_field(name="Атмосферное давление(hPa)", value=f"**{current_pressure}hPa**", inline=False)
    embed.set_thumbnail(url="https://i.ibb.co/CMrsxdX/weather.png")
    embed.set_footer(text=f"Requested by {ctx.author.name}")

    await channel.send(embed=embed)

