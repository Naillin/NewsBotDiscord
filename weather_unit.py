class WeatherUnit:
    def __init__(self, weather_description, temperature, humidity, pressure):
        self.weather_description = weather_description
        self.temperature = temperature
        self.humidity = humidity
        self.pressure = pressure

    def __str__(self):
        return self.weather_description
