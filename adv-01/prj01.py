######################匯入模組###############################
from tkinter import *

######################建立視窗###############################
windows = Tk()


######################定義函式###############################
def hi_fun():
    print("sb")


######################建立按鈕###############################
btn1 = Button(windows, text="??????????", command=hi_fun)
btn1.pack()
windows.title("My First GUI")
######################建立標籤###############################
disaplay = Label(windows, text="?!@#$", fg="red", bg="black")

disaplay.pack()
######################運行應用程式###############################
windows.mainloop()
