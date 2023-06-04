from tkinter import Tk

from advancedtkinter.timeViews import Calendar

tk=Tk()
c=Calendar(bg="#08415C")
#c.addBadge(1,1,"30","#ff00ff")
c.pack()
from datetime import datetime
def examplemarkerfunction(y,m):

    print(datetime.today().strftime('%Y-%m')==f"{c.year}-{c.month}",datetime.today().strftime('%Y-%m'),f"{c.year}-{c.month}")
    if datetime.today().strftime('%Y-%m')==f"{y}-{str(m).zfill(2)}":
        return {int(datetime.today().strftime('%d')):"red"}

    return {20:"#ff00ff",12:"#00ffff"}

def onclick(date):

    print("youclicked ",date)


c.StandartCalder([2023,2],getMarkersFunction=examplemarkerfunction,onDayClicked=onclick)
tk.mainloop()