import requests
import openai
import discord


class WeatherAPI:

    def __init__(self, api_key, units="metric", lang="zh_tw"):
        self.api_key = api_key
        self.units = units
        self.lang = lang
        self.base_url = "http://api.openweathermap.org/data/2.5/weather?"
        self.forecast_url = "http://api.openweathermap.org/data/2.5/forecast?"
        self.icon_base_url = "https://openweathermap.org/img/wn/"

    def get_current_weather(self, city_name):
        send_url = f"{self.base_url}q={city_name}&appid={self.api_key}&units={self.units}&lang={self.lang}"
        response = requests.get(send_url)
        return response.json()

    def get_forecast(self, city_name):
        send_url = f"{self.forecast_url}q={city_name}&appid={self.api_key}&units={self.units}&lang={self.lang}"
        response = requests.get(send_url)
        response.raise_for_status()
        return response.json()

    def get_icon_url(self, icon_code):
        return f"{self.icon_base_url}{icon_code}@2x.png"

    def get_icon(self, icon_code):

        icon_url = self.get_icon_url(icon_code)
        response = requests.get(icon_url)
        if response.status_code == 200:
            return response.content
        else:
            return None

    async def create_weather_embed(self, city, weather_info):
        unit_symbol = "C" if self.units == "metric" else "F"
        if "weather" in weather_info and "main" in weather_info:
            current_temperature = weather_info["main"]["temp"]
            weather_description = weather_info["weather"][0]["description"]
            icon_code = weather_info["weather"][0]["icon"]
            icon_url = self.get_icon_url(icon_code)
            embed = discord.Embed(
                title=f"{city} 天氣",
                description=f"描述：{weather_description}",
                color=0x1E90FF,
            )
            embed.set_thumbnail(url=icon_url)
            embed.add_field(
                name="氣溫", value=f"{current_temperature}{unit_symbol}", inline=False
            )
            return embed
        return None

    async def create_forecast_embed(self, city, forecast_info):
        unit_symbol = "C" if self.units == "metric" else "F"
        embeds = []
        if "list" in forecast_info:
            forecast_list = forecast_info["list"][:10]
            for forecast in forecast_list:
                dt_txt = forecast["dt_txt"]
                temp = forecast["main"]["temp"]
                description = forecast["weather"][0]["description"]
                icon_code = forecast["weather"][0]["icon"]
                icon_url = self.get_icon_url(icon_code)
