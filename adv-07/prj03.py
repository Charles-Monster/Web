from ttkbootstrap import *
import sys
import os
from PIL import Image, ImageTk
import requests
import datetime
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties

#######################設定工作目錄########################
os.chdir(sys.path[0])  # 設定工作目錄
#######################定義常數########################
API_KEY = "892da2f13edf3c7f382637760e72d224"  # API Key
BASE_URL = "http://api.openweathermap.org/data/2.5/weather?"  # API URL
FORECAST_URL = "http://api.openweathermap.org/data/2.5/forecast?"  # 5 Day / 3 Hour Forecast API URL
UNITS = "metric"  # 單位 (公制)
LANG = "zh_tw"  # 語言 (繁體中文)
ICON_BASE_URL = "https://openweathermap.org/img/wn/"  # 天氣圖標基礎 URL


#######################定義函數########################
def get_weather_info():
    global UNITS, current_temperature
    city_name = city_name_entry.get()
    send_url = f"{BASE_URL}appid={API_KEY}&q={city_name}&units={UNITS}&lang={LANG}"
    response = requests.get(send_url)
    info = response.json()
    if "weather" in info and "main" in info:
        current_temperature = info["main"]["temp"]
        weather_description = info["weather"][0]["description"]
        icon_code = info["weather"][0]["icon"]
        icon_url = f"{ICON_BASE_URL}{icon_code}@2x.png"
        icon_response = requests.get(icon_url)
        if icon_response.status_code == 200:
            with open(f"{icon_code}.png", "wb") as icon_file:
                icon_file.write(icon_response.content)
        image = Image.open(f"{icon_code}.png")
        tk_image = ImageTk.PhotoImage(image)
        icon_label.config(image=tk_image)
        icon_label.image = tk_image
        temperature_label.config(
            text=f"溫度: {current_temperature}°{'C' if UNITS == 'metric' else 'F'}"
        )
        description_label.config(text=f"描述: {weather_description}")
        # 繪製並顯示圖表
        draw_graph(city_name)
    else:
        description_label.config(text="描述: 找不到該城市")


def draw_graph(city_name):
    send_url = f"{FORECAST_URL}q={city_name}&appid={API_KEY}&units={UNITS}&lang={LANG}"
    response = requests.get(send_url)
    response.raise_for_status()  # 檢查請求是否成功
    info = response.json()
    # 準備繪圖數據
    xlist = []  # 準備 x 軸數據
    ylist = []  # 準備 y 軸數據
    if "city" in info:
        # 處理並顯示天氣預報
        for forecast in info["list"]:
            dt_txt = forecast["dt_txt"]  # 預報時間
            temp = forecast["main"]["temp"]  # 預報溫度
            time = datetime.datetime.strptime(dt_txt, "%Y-%m-%d %H:%M:%S").strftime(
                "%m/%d %H"
            )  # 格式化時間
            xlist.append(time)
            ylist.append(temp)
    else:
        print("找不到該城市或無法獲取天氣資訊")
    #######################繪製圖表########################
    font = FontProperties(
        fname="NotoSansTC-Black.otf", size=14
    )  # 設定字型這樣才能顯示中文
    fig, ax = plt.subplots(figsize=(12, 6))  # 設定圖表大小, 單位是英寸
    ax.plot(xlist, ylist)  # 使用軸對象繪製圖表
    ax.set_title("7 天氣溫預測", fontproperties=font)
    ax.set_ylabel("溫度 (°C)", fontproperties=font)
    ax.set_xlabel("日期", fontproperties=font)
    plt.xticks(rotation=45)  # 旋轉 x 軸標籤以避免重疊
    plt.tight_layout()  # 自動調整佈局
    fig.savefig("weather_forecast.png")  # 儲存圖表
    plt.close()  # 關閉圖表以釋放記憶體
    # 在 Canvas 上顯示圖片
    image = Image.open("weather_forecast.png")
    img = ImageTk.PhotoImage(image)
    # 重新設定畫布大小
    canvas.config(width=image.width, height=image.height)
    canvas.create_image(
        image.width // 2, image.height // 2, image=img
    )  # 在畫布上顯示圖片
    canvas.image = img  # 保持對圖片的引用，防止被垃圾回收


def on_switch_change():
    global UNITS, current_temperature
    UNITS = "metric" if check_type.get() else "imperial"
    if temperature_label["text"] != "溫度: ?°C":
        if UNITS == "metric":
            current_temperature = round((current_temperature - 32) * 5 / 9, 2)
        else:
            current_temperature = round(current_temperature * 9 / 5 + 32, 2)
        temperature_label.config(
            text=f"溫度: {current_temperature}°{'C' if UNITS == 'metric' else 'F'}"
        )


#######################建立視窗########################
window = tk.Tk()
window.title("Weather App")
#######################設定字型########################
font_size = 20
window.option_add("*font", ("Helvetica", font_size))
#######################設定主題########################
style = Style(theme="minty")
style.configure("my.TButton", font=("Helvetica", font_size))
style.configure("my.TCheckbutton", font=("Helvetica", font_size))
#######################建立變數########################
check_type = BooleanVar()
check_type.set(True)
#######################建立標籤########################
city_name_label = Label(window, text="請輸入想搜尋的城市:")
city_name_label.grid(row=0, column=0)
icon_label = Label(window, text="天氣圖標")
icon_label.grid(row=1, column=0)
temperature_label = Label(window, text="溫度: ?°C")
temperature_label.grid(row=1, column=1)
description_label = Label(window, text="描述: ?")
description_label.grid(row=1, column=2)
#######################建立輸入框########################
city_name_entry = Entry(window)
city_name_entry.grid(row=0, column=1)
#######################建立按鈕########################
search_button = Button(
    window, text="獲得天氣資訊", command=get_weather_info, style="my.TButton"
)
search_button.grid(row=0, column=2)
#######################建立Checkbutton########################
check = Checkbutton(
    window,
    variable=check_type,
    onvalue=True,
    offvalue=False,
    command=on_switch_change,
    style="my.TCheckbutton",
    text="溫度單位(°C/°F)",
)
check.grid(row=2, column=1, padx=10, pady=10)
#######################創建畫布#######################
canvas = Canvas(window, width=0, height=0, bg="white")
canvas.grid(row=3, column=0, columnspan=3, padx=10, pady=10)
#######################運行應用程式########################
window.mainloop()
