from tkinter import *
from advancedtkinter import tkinterML,independentComponents as indp,chat,gameUiComponents

tk=Tk()

tkinterML.addEquivelent("betterbutton",indp.BetterButton)  #used to add Custom Elements to the Page-elemmts



switchframe=indp.swithchFrame(master=tk)

switchframe.pack()

pageframe1=tkinterML.PageFrame(master=switchframe,path="testpage")

frameid1=switchframe.puschFrame(pageframe1) #adding 'pageframe1' to the pagelist of 'switchframe'

switchframe.show(frameid1)   # setting the visible frame

tk.mainloop()