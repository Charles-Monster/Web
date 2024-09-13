######################匯入模組###############################
from tkinter import *
from PIL import Image, ImageTk
import sys
import os

######################設定工作目錄###############################
os.chdir(sys.path[0])
######################建立視窗###############################
windows = Tk()
windows.title("My Second GUI")
######################創建畫布###############################
canvas = Canvas(windows, width=600, height=600, bg="white")
canvas.pack()
######################設定視窗圖片###############################
# windows.iconbitmap("crocodile2.ico")
######################載入圖片###############################
img = Image.open("crocodile2.gif")
img = ImageTk.PhotoImage(img)
######################顯示圖片###############################
my_img = canvas.create_image(300, 300, image=img)
######################運行應用程式###############################
windows.mainloop()
