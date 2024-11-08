import requests


class WeatherAPI:
    def __init__(self, api_key, units="metric", lang="zh_tw"):
        self.api_key = api_key
        self.units = units
        self.lang = lang
        self.base_url = "https://api.openweathermap.org/data/2.5/weather?"
        self.forecast_url = "https://api.openweathermap.org/data/2.5/forecast?"
        self.icon_base_url = "https://openweathermap.org/img/wn/"

    def get_current_weather(self, city_name):
        send_url = f"{self.base_url}appid={self.api_key}&q={city_name}&units={self.units}&lang={self.lang}"
        response = requests.get(send_url)
        response.response.json()

    def get_forecast(self, city_name):
        send_url = f"{self.forecast_url}q={city_name}&appid={self.api_key}&units={self.units}&lang={self.lang}"
        response = requests.get(send_url)
        response.raise_for_status()
        return response.json()
