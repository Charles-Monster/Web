######################匯入模組###############################
from tkinter import *

######################建立視窗###############################
windows = Tk()


######################定義函式###############################
def hi_fun():
    print("")
    global change
    if change == False:
        disaplay.config(text="save", fg="black", bg="green")
    else:
        disaplay.config(text="rip", fg="black", bg="red")
    change = not change


change = False

######################建立按鈕###############################
btn1 = Button(windows, text="在三秒內按下訂閱鍵，否則你有生命危險", command=hi_fun)
btn1.pack()
windows.title("My First GUI")

######################建立標籤###############################
disaplay = Label(windows, text="save", fg="black", bg="green")
disaplay.pack()

######################運行應用程式###############################
windows.mainloop()
