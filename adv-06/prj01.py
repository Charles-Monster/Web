import requests

#####################定義常數#######################
API_KEY = "5a67c8c7f697cf6dc00b249ed3d17572"
BASE_URL = "https://api.openweathermap.org/data/2.5/weather?"
UNITS = "metric"
LANG = "zh_tw"
#####################主程式#######################
city_name = "Maynila"
send_url = f"{BASE_URL}&q={city_name}appid={API_KEY}&units={UNITS}&lang={LANG}"

print(f"發送的URL：{send_url}")
response = requests.get(send_url)
response.raise_for_status()
info = response.json()
if "city" in info:
    for forecast in info["list"]:
        dt_txt = forecast["dt_txt"]
        temp = forecast["main"]["temp"]
        weather_description = forecast["weather"][0]["description"]
        print(f"日期：{dt_txt}-溫度：{temp}℃,天氣狀況：{weather_description}")
else:
    print("找不到該程式或無法獲取資訊")
