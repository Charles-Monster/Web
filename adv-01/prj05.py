######################匯入模組###############################
from tkinter import *
import random

######################建立視窗###############################
windows = Tk()


######################定義函式###############################
def hi_fun():
    # print("")
    # global change
    # if change == False:
    #     random.randint(1, 2)
    #     if random.randint(1, 2) == 1:
    #         disaplay.config(text="save", fg="black", bg="green")
    #     else:
    #         disaplay.config(text="rip", fg="black", bg="red")
    # else:
    #     random.randint(1, 2)
    #     if random.randint(1, 2) == 1:
    #         disaplay.config(text="save", fg="black", bg="blue")
    #     else:
    #         disaplay.config(text="rip", fg="black", bg="orange")
    # change = not change
    disaplay.config(text="save", fg=random.choice(COLARS))


COLARS = [
    "red",
    "green",
    "blue",
    "yellow",
    "orange",
    "purple",
    "pink",
    "brown",
    "black",
    "white",
]


######################建立按鈕###############################
btn1 = Button(windows, text="在三秒內按下訂閱鍵，否則你有生命危險", command=hi_fun)
btn1.pack()
windows.title("My First GUI")

######################建立標籤###############################
disaplay = Label(windows, text="save", fg="black", bg="green")
disaplay.pack()

######################運行應用程式###############################
windows.mainloop()
