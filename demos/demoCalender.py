from tkinter import Tk

from advancedtkinter.timeViews import Calendar

tk=Tk()
c=Calendar(bg="#08415C")
#c.addBadge(1,1,"30","#ff00ff")
c.pack()

def examplemarkerfunction(y,m):
    return {20:"#ff00ff",12:"#00ffff"}

def onclick(day):
    print("youclicked ",day)

c.StandartCalder([2023,2],getMarkersFunction=examplemarkerfunction,onDayClicked=onclick)
tk.mainloop()