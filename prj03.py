######################匯入模組###############################
from tkinter import *

######################建立視窗###############################
windows = Tk()


######################定義函式###############################
def hi_fun():
    print("Cola is good")
    disaplay.config(text="", fg="red", bg="black")


def clear_fun():
    disaplay.config(text="?!@#$", fg="red", bg="black")


######################建立按鈕###############################
btn1 = Button(windows, text="可樂是好東西", command=hi_fun)
btn1.pack()
btn2 = Button(windows, text="可樂萬歲", command=clear_fun)
btn2.pack()
windows.title("My First GUI")

######################建立標籤###############################
disaplay = Label(windows, text="coca cola zero sugar", fg="red", bg="black")

disaplay.pack()
######################運行應用程式###############################
windows.mainloop()
