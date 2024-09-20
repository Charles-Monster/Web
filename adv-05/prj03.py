from ttkbootstrap import *
import sys
import os
from PIL import Image, ImageTk
import requests

#################設定工作目錄#######################
os.chdir(sys.path[0])

####################定義常數####################
API_KEY = "5a67c8c7f697cf6dc00b249ed3d17572"
BASE_URL = "https://api.openweathermap.org/data/2.5/weather?"
UNITS = "metric"
LANG = "zh_tw"
ICON_BASE_URL = "https://openweathermap.org/img/wn/"


#################定義函數#######################
def on_switch_change():
    check_label.config(text=str(check_type.get()))


#################建立視窗#######################
window = tk.Tk()
window.title("Weather app")
#################設定自型#######################
font_sive = 20
window.option_add("*Font", ("Helvetica", font_sive))
##################建立變數#######################
check_type = BooleanVar()
check_type.set(True)
##################顯示圖片#######################
image = Image.open(f"{icon.png}.pmg")
tk_image = ImageTk.PhotoImage(image)
icon_label.config(image=tk_image)
icon_label.image = tk_image
#################建立標籤#######################
city_name_label = Label(window, text="城市名稱")
city_name_label.grid(row=0, column=0)
icon_label = Label(window, text="天氣圖標")
icon_label.grid(row=1, column=0)

temprature_label = Label(window, text="溫度:?℃")
temprature_label.grid(row=1, column=1)

description_label = Label(window, text="描述")
description_label.grid(row=1, column=2)

#####################建立輸入框#######################
city_name_entry = Entry(window)
city_name_entry.grid(row=0, column=1)
########################建立按鈕#######################
search_button = Button(window, text="獲得天氣資訊"
command=get_weather_info,style="my.TButton")
search_button.grid(row=0, column=2)
#####################建立Checkbutton#######################
check = Checkbutton(
    window,
    variable=check_type,
    onvalue=True,
    offvalue=False,
    command=on_switch_change,
    style="溫度單位(℃/℉)",
)
check.grid(row=2, column=1, padx=10, pady=10)
#####################運行應用程式#######################
window.mainloop()
