######################匯入模組###############################
from tkinter import *
from PIL import Image, ImageTk
import sys
import os

######################設定工作目錄###############################
os.chdir(sys.path[0])


######################定義函式###############################
def move_object(event, object, dx, dy):
    canvas.move(object, dx, dy)


######################建立視窗###############################
windows = Tk()
windows.title("My Second GUI")
######################建立按鈕###############################
quit_btn = Button(windows, text="Quit", command=move_object)
quit_btn.pack()
######################創建畫布###############################
canvas = Canvas(windows, width=600, height=600, bg="white")
canvas.pack()
######################設定視窗圖片###############################
# windows.iconbitmap("crocodile2.ico")
######################載入圖片###############################
img = Image.open("crocodile2.gif")
img = ImageTk.PhotoImage(img)
######################畫圖形###############################
circle = canvas.create_oval(250, 150, 300, 200, fill="green")
rect = canvas.create_rectangle(220, 400, 340, 430, fill="blue")
msg = canvas.create_text(
    300,
    100,
    text="mario,your head is green,馬力歐，你的頭真綠",
    fill="green",
    font=("Arial", 10),
)
#####################綁定按鍵事件###############################
canvas.bind_all("<Right>", lambda event: move_object(event, circle, 10, 0))
canvas.bind_all("<Left>", lambda event: move_object(event, circle, -10, 0))
canvas.bind_all("<Up>", lambda event: move_object(event, circle, 0, -10))
canvas.bind_all("<Down>", lambda event: move_object(event, circle, 0, 10))
canvas.bind_all("<d>", lambda event: move_object(event, rect, 10, 0))
canvas.bind_all("<a>", lambda event: move_object(event, rect, -10, 0))
canvas.bind_all("<w>", lambda event: move_object(event, rect, 0, -10))
canvas.bind_all("<s>", lambda event: move_object(event, rect, 0, 10))


######################顯示圖片###############################
my_img = canvas.create_image(300, 250, image=img)
######################運行應用程式###############################
windows.mainloop()
