import os
import sys
from html.parser import HTMLParser
from tkinter import *
import tkinter.ttk as Ttk
from tkinter import font as f
from . import *
from .staticPy import Collor
from . import independentComponents as Comp
from .gameUiComponents import *

from _tkinter import TclError

altanertiveNames={"div":Frame,"optionbutton":OptionButton}



def addEquivelent(htmtk_element_name,pythonic_name):
    altanertiveNames[htmtk_element_name]=pythonic_name


class MyHTMLParser(HTMLParser):
    def aplyArtSelf(self,pypage,shared):

        self.tk:Tk=None
        self.tagStack = []
        self.idl = {}
        self.sharedDict=shared
        self.page=pypage
        self.namel={}
        self.id=0

    def handle_starttag(self, tag, attrs):#
        if "id" in attrs:
            id=None
        if "style" in attrs:
            style=None
        if tag.lower()=="window":
            self.createWindow()
            #self.tagStack.append(c)
        else :
            try:
                if not tag in altanertiveNames:
                    tag = tag.capitalize()

                c=self.createElement(tag,kwwargs=attrs)
            except IOError as e:
                pos=self.getpos()
                raise Exception(f"tag-{e.args[0]} in line {pos[0]} char {pos[1]}")

            self.tagStack.append(c)


        #self.tagStack.append(c)
        print("Encountered a start tag:", tag,attrs)

    def handle_endtag(self, tag):
        self.tagStack.pop(-1)
        print("Encountered an end tag :", tag)

    def handle_data(self, data):
        if data.strip(" ").strip("\n")!="":
            print(".",data,".")
            try:
                self.namel[self.tagStack[-1]].configure(text=data)
            except TclError:
                pass

        print("Encountered some data  :", data)



    def createWindow(self):
        name = "#" + str(self.id)
        self.id += 1
        tk=Tk()
        tk.configure()
        self.tagStack+=["."]
        self.tk=tk
        self.namel["."]=tk
        print(tk)

    def setmaster(self,master):
        name = "#" + str(self.id)
        self.id += 1
        self.tk=master
        self.tagStack += ["."]
        self.namel["."] = master


    def getartoftype(self,array,type):
        for a in array:
            if a[0]==type:
                return a[1]
        return False


    def createElement(self,tag,kwwargs,id=None):
        l=None

        name="#"+str(self.id)
        self.id+=1

        tag=tag.replace("@",".")
        master=self.tagStack[-1]
        if master==".":
            master="None"
        styleart:str=self.getartoftype(kwwargs,"style")

        id =self.getartoftype(kwwargs,"id")
        sh=self.sharedDict

        if styleart:
            if styleart.endswith(","):
                styleart=styleart[:-1]
            if styleart.startswith(","):
                styleart=styleart[1:]
            try:
                print(name,tag)

                self.namel[name]=eval(tag + "(master=self.namel['"+self.tagStack[-1]+"'],name='"+name+"',"+styleart+")",altanertiveNames)
            except NameError as e:

                exec ("self.namel['"+name+"']="+tag + "(master=self.namel['"+self.tagStack[-1]+"'],name='"+name+"',"+styleart+")")


            except SyntaxError as e:
                pos = self.getpos()
                raise Exception(f"Invalid syntax in style declarator in line {pos[0]} {repr(e)}")
            except KeyError as e:

                pos = self.getpos()

                raise Exception("Dict doesnt contain key",e,f"in line {pos[0]}   {repr(e)}")
        else:
            print(self.tagStack)
            print()
            self.namel[name]=eval(tag + "(master=self.namel['"+self.tagStack[-1]+"'],name='"+name+"' )", {**altanertiveNames,"self":self,"Collor":Collor})

        ifstatement=self.getartoftype(kwwargs,"if")

        ly:str=self.getartoftype(kwwargs,"ly")
        innercondition=""

        if ly:
            ll = ly.split(":")
            if len(ll)<2:
                match ll[0]:
                    case "pack":
                        self.namel[name].pack()
                    case "grid":
                        self.namel[name].grid()
                    case "place":
                        self.namel[name].place()
            else:
                print("kfkoewqjkopfjrewjopjopfre",ll)
                innercondition=ll[1]
                exec("self.namel['"+name+"']."+ll[0]+"("+ll[1]+")")
        else:
            self.namel[name].pack()

        def check_for_bindings(name,l):
            for a in l:
                if  (a[0].startswith("(")&a[0].endswith(")")):
                    eventname=a[0][1:-1]

                    try:
                        print(eventname)
                        func=a[1].replace("$event","event")
                        print(func)
                        page=self.page
                        sh=self.sharedDict
                        self.namel[name].bind("<"+eventname.capitalize()+">",lambda event:eval(func,{"page":self.page,"event":event,"sh":self.sharedDict}))

                    except ImportError:
                        raise Exception(f"Unknown binding for event'<{eventname.capitalize()}>' in line "+str(self.getpos()[0]))
        check_for_bindings(name,kwwargs)
        if ifstatement:
            if ly:
                onshow= f"self.namel['"+name+f"'].{ll[0]}({innercondition})"
                onforget= f"self.namel['"+name+f"'].{ll[0]}_forget()"
            else:
                onshow = f"self.namel['" + name + f"'].pack()"
                onforget = f"self.namel['" + name + f"'].pack_forget()"

            def setvisible(condition,onshow="pass",onhide="pass"):
                page=self.page
                if eval(condition):
                    exec(onshow)
                else:
                    exec(onhide)

                self.tk.after(100,lambda :setvisible(condition,))
            setvisible(ifstatement,onshow=onshow,onhide=onforget)
        if id:
            self.idl[id]=l
        if id:
            self.idl[id] = self.namel[name]
        return name
    def getbyId(self,id):
        try:
            return self.idl[id]
        except KeyError:
            raise Exception("Id '"+str(id)+"' referenced before being assign to element in ")

    def setobj_dict(self,d:dict):
        self.namel=d
        pass


class PageFrame(Frame):
    def __init__(self,master,path="testpage\\page.htmtk",sharedDict=None,**kwargs):
        Frame.__init__(self,master=master,**kwargs)
        self.parser = MyHTMLParser()
        sppath=path[::-1].split("\\",1)
        if len(sppath)>1:
            pp=path[::-1].split("\\",1)[1][::-1]
        else:
            pp=path
            if  ( (not path.endswith("\\"))& (not path.endswith("/"))):
                pp+="\\"
                path+="\\"
            print(pp)

        sys.path.insert(0,pp)
        i =__import__("page")

        objdict={}

        self.parser.aplyArtSelf(pypage=i.page(objdict,sharedDict),shared=sharedDict)
        self.parser.setobj_dict(objdict)
        self.parser.setmaster(self)

        with open(path+"page.htmtk",encoding="utf8") as file:
            self.parser.feed(file.read())

        #self.parser.tk.mainloop()

if __name__=="__main__":
    tk=Tk()
    PageFrame(tk)
    tk.mainloop()


