class Observable:
    def __init__(self,value,returntype,prefix="",subfix=""):
        self.subfix = subfix
        self.prefix = prefix
        self.__value = value
        self.returntype = returntype
        self.alarms=[]
        self.alarmsRaw=[]
    def sv(self, value):
        self.__value=value
        for arlarm in self.alarms:
            arlarm(self.gv())
        for arlarm in self.alarmsRaw:
            arlarm(value)
    def gv(self):

        if self.returntype:
            val=self.returntype(self.__value)
        else:
            val=self.__value
        if (type(self.__value)==str)|(self.returntype==str):
            return self.prefix+ val+self.subfix
        return self.__value

    def gvR(self):
        return self.__value
    def __setattr__(self, key, value):
        #print("setAttribute",key)
        if key=="value":
            self.__dict__["_Observable__value"]=value
            for arlarm in self.alarms:
                arlarm(self.gv())
            for arlarm in self.alarmsRaw:
                arlarm(value)
        else:
            self.__dict__[key]=value

    def __getattr__(self, item):

        if item == "value":
            return self.__dict__["_Observable__value"]

        else:
            return self.__dict__[item]

    def subscribe(self,alarm):
        self.alarms.append(alarm)

    def subscribeRaw(self, alarm):
        self.alarmsRaw.append(alarm)
