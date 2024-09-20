import json
import requests

# json_str = json.dumps(data)
# json_data = json.loads(json_str)
####################定義常數####################
API_KEY = "5a67c8c7f697cf6dc00b249ed3d17572"
BASE_URL = "https://api.openweathermap.org/data/2.5/weather?"
UNITS = "metric"
LANG = "zh_tw"
####################主程式####################
city_name = input("請輸入城市名稱：")
send_url = f"{BASE_URL}appid={API_KEY}&q={city_name}&units={UNITS}&lang={LANG}"
print(f"發送的URL：{send_url}")
response = requests.get(send_url)
info = response.json()
if "weather" in info and "main" in info:
    current_temperature = info["main"]["temp"]
    weather_description = info["weather"][0]["description"]
    print(f"城市: {city_name}")
    print(f"當前溫度：{current_temperature}℃")
    print(f"描述：{weather_description}")
else:
    print("查詢失敗")
