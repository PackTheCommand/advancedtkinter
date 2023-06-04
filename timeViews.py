
from tkinter import Canvas, Tk,font
import calendar as cale

class Calendar(Canvas):
    def __init__(self, tfont=None,fontfg="#ffffff", **kwargs):
        Canvas.__init__(self,**kwargs)

        if tfont==None:
            tfont=font.Font(family="Calibre", size=20)
        self.colums=7
        self.fontfg=fontfg
        self.font=tfont
        self.badgeZ=40

        self.textMargin=8
        self.spacing=5
        self.colidebles={}
        self.bind("<Button-1>",self._colisions)


    def _colisions(self,e):
        x,y=e.x,e.y
        for func in self.colidebles:
            for value in self.colidebles[func]:
                x1,y1,x2,y2=self.bbox(value)
                if (x1<x<x2)&(y1<y<y2):
                    print("Value",value)
                    if func:

                        func(value)
                    return
                pass

    def _create_round_rectangle(self, x1, y1, x2, y2, radius=25, **kwargs):
        points = [x1 + radius, y1, x1 + radius, y1, x2 - radius, y1, x2 - radius, y1,
                  x2, y1, x2, y1 + radius, x2, y1 + radius, x2, y2 - radius,
                  x2, y2 - radius, x2, y2, x2 - radius, y2, x2 - radius, y2, x1 + radius, y2,
                  x1 + radius, y2, x1, y2, x1, y2 - radius, x1, y2 - radius, x1, y1 + radius,
                  x1, y1 + radius, x1, y1]

        return self.create_polygon(points, **kwargs, smooth=True)
    def _topBar(self,width,title,font,height=30,textmarginx=10,bg="#83C9F4"):
        bgr=self._create_round_rectangle(0,0,width,30,fill=bg)
        ca=self.create_text(textmarginx,0, anchor="nw", text=title, font=font,
                         fill=self.fontfg)
        a4 = self.bbox(ca)
        cax = a4[2] - a4[0]

        cay = a4[3] - a4[1]
        print("gds", cax, cay)

        margin_y = (height - cay) // 2

        self.moveto(ca, x=textmarginx, y=margin_y)

        def trigerBack(i):
            self.event_generate("<<Last>>")
        def trigerForth(i):
            self.event_generate("<<Next>>")

        c=self.create_text(width-(textmarginx+40), margin_y, anchor="nw", text="ᐸ", font=font,
                         fill=self.fontfg)
        self.addclickables(trigerBack,c)
        c1=self.create_text(width-(textmarginx+20), margin_y, anchor="nw", text="ᐳ", font=font,
                         fill=self.fontfg)
        self.addclickables(trigerForth, c1)

        return [ca,bgr,c,c1]

    def _bindTBClicks(self):
        pass
    def addclickables(self,func,obj):
        if func in self.colidebles.keys():
            self.colidebles[func]+=[obj]
            return
        self.colidebles[func]= [obj]
    def addBadge(self,xr,yr,day,color,click=None):
        xb,yb=20,40
        setx=xb+(xr*self.badgeZ)+(self.spacing*xr)
        sety=yb+(yr*self.badgeZ)+(self.spacing*yr)
        print(setx,sety)
        c=self._create_round_rectangle(setx,sety,setx+self.badgeZ,sety+self.badgeZ,fill=color,radius=10)
        self.addclickables(click,c)
        ca=self.create_text(setx+self.textMargin,sety+self.textMargin,anchor="nw",text=day,font=self.font,fill=self.fontfg)
        a4=self.bbox(ca)
        cax=a4[2]-a4[0]

        cay = a4[3]-a4[1]
        print("gds",cax,cay)
        margin_x=(self.badgeZ-cax)//2
        margin_y = (self.badgeZ - cay) // 2

        self.moveto(ca,x=setx+margin_x,y=sety+margin_y)
        return [c,ca]

    def delItems(self,ids):
        print(ids)
        for id in ids:
            self.delete(id)
            for func in self.colidebles:
                 if id in self.colidebles[func]:
                     self.colidebles[func].remove(id)




    def genCal(self,weeks,marks={},defuldCollor="#83C9F4",onclicl=None):

        l=[]

        def oncl(id):
            print("l34",l)

            if onclicl:
                onclicl(l.index(id)//2+1)

        for n,week in enumerate(weeks):
            print(week)
            for n2,day in enumerate(week):

                if day==0:
                    continue


                day=day
                if day in marks.keys():
                    l+=self.addBadge(n2,n,day=str(day),color=marks[day],click=oncl)
                else:
                    l+=self.addBadge(n2,n, day=str(day), color=defuldCollor,click=oncl)
        print("l",l)
        return l

    def StandartCalder(self,date:[int,int],getMarkersFunction:{}=None,onDayClicked=None,badgeColor="#83C9F4",tbbg="#83C9F4"):
        year=date[0]
        month=date[1]
        def ondKlick(d):
            if onDayClicked:
                onDayClicked((d,month,year))
        self.update()
        def getmarks()->dict:
            if getMarkersFunction:
                return getMarkersFunction(year, month)
            return {}
        tb=self._topBar(self.winfo_width(), "March", font=font.Font(size=10, font="Calibre", weight="bold"),bg=tbbg)
        monthNames=["","January","February","March","April","May","June","July","August","September","Oktober","November","December"]
        rc = cale.monthcalendar(year,month)
        comps=self.genCal(rc,marks=getmarks(),onclicl=ondKlick,defuldCollor=badgeColor)

        self.itemconfig(tb[0],text=monthNames[month]+f" {year}")


        def next(u):
            nonlocal month,rc,comps,year
            if 0<month<12:
                month+=1

            elif month==12:
                month=1
                year+=1
            rc = cale.monthcalendar(year, month)
            self.delItems(comps)
            self.itemconfig(tb[0],text=monthNames[month]+f" {year}")
            comps = self.genCal(rc,marks=getmarks(),onclicl=ondKlick,defuldCollor=badgeColor)

        def last(u):
            nonlocal month, rc, comps, year

            if month == 1:
                month = 12
                year -= 1
            else:
                month -= 1

            rc = cale.monthcalendar(year, month)
            self.delItems(comps)
            self.itemconfig(tb[0], text=monthNames[month] + f" {year}")
            comps = self.genCal(rc,marks=getmarks(),onclicl=ondKlick,defuldCollor=badgeColor)



        self.bind("<<Next>>",next)
        self.bind("<<Last>>", last)





