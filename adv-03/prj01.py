from ttkbootstrap import *
import sys
import os

################設定工作目錄###############
os.chdir(sys.path[0])


#################定義函式#################
def show_result():
    entry_text = entry.get()
    try:
        result = eval(entry_text)
    except:
        result = "請輸入正確的計算式"
    label.config(text=result)


#################建立視窗#################
window = tk.Tk()
window.title("My GUI")
#################設定自型#################
font_sive = 20
window.option_add("*Font", ("Helvetica", font_sive))
#################設定主題#################
style = Style(theme="minty")
style.configure("my.TButton", font=("Helvetica", font_sive))
#################建立標籤#################
# label = Label(window, text="選擇檔案")
# label.grid(row=0, column=0, sticky="E")
# label2 = Label(window, text="無")
# label.grid(row=0, column=1, sticky="E")
label = Label(window, text="計算結果")
label.grid(row=2, column=0, columnspan=2, padx=10, pady=10)
#################建立按鈕#################
# button = Button(window, text="瀏覽", command=open_file, style="my.TButton")
# button.grid(row=0, column=2, sticky="W")
# button2 = Button(window, text="顯示", command=show_image, style="my.TButton")
# button2.grid(row=1, column=3, sticky="EW")
# canvas = Canvas(window, width=600, height=600)
# canvas.grid(row=2, column=0, columnspan=3)
button = Button(window, text="顯示計算結果", command=show_result, style="my.TButton")
button.grid(row=1, column=0, columnspan=2, padx=10, pady=10)
#################建立Entry物件#################
entry = Entry(window, width=30)
entry.grid(row=0, column=0, columnspan=2, padx=10, pady=10)
#################運行應用程式##############
window.mainloop()
