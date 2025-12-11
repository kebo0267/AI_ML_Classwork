import base64
import json
from datetime import datetime, timedelta

class TaskInfo:
    def __init__(self):
        self.info = {}
        self.info["taskName"] = ""
        self.info["taskId"] = ""
        self.info["description"] = ""
        self.info["taskCreateDate"] = datetime.now()
        self.info["taskUpdateDate"] = datetime.now()
        self.info["taskCompleteDate"] = datetime(1967,2,6,0,0,0)
        self.info["createUser"] = ""
        self.info["updateUser"] = ""
        self.info["status"] = "Pending"
        
        self.dateFormat = "%Y-%m-%d %H:%M:%S"
        self.altDateFormat = "%Y-%m-%d"

    def getDateTimeFormat(self):
        return self.altDateFormat
    @property
    def taskName(self):
        return self.info["taskName"]
    
    @taskName.setter
    def taskName(self,new_taskName):
        self.info["taskName"] = new_taskName

    @property
    def description(self):
        return self.info["description"]
    
    @description.setter
    def description(self,new_desc):
        self.info["description"] = new_desc

    @property
    def taskId(self):
        return self.info["taskId"]
    
    @taskId.setter
    def taskId(self,new_taskId):
        self.info["taskId"] = new_taskId

    @property
    def createUser(self):
        return self.info["createUser"]
    
    @createUser.setter
    def createUser(self,new_createUser):
        self.info["createUser"] = new_createUser

    @property
    def updateUser(self):
        return self.info["updateUser"]
    
    @updateUser.setter
    def updateUser(self,new_updateUser):
        self.info["updateUser"] = new_updateUser

    @property
    def status(self):
        return self.info["status"]
    
    @status.setter
    def status(self,new_status):
        self.info["status"] = new_status

    @property
    def taskCreateDate(self):
        return self.info["taskCreateDate"]

    @property
    def taskUpdateDate(self):
        return self.info["taskUpdateDate"]

    @property
    def taskCompleteDate(self):
        return self.info["taskCompleteDate"]
    

    def set_taskCreateDate(self,timeStr=None):
        if timeStr == None:
            self.info["taskCreateDate"] = datetime.now()
        elif type(timeStr) == datetime:
            self.info["taskCreateDate"] = timeStr
        else:
            try:
                self.info["taskCreateDate"] = datetime.strptime(timeStr,self.dateFormat)
            except ValueError as e:
                try:
                    self.info["taskCreateDate"] = datetime.strptime(timeStr,self.altDateFormat)
                except ValueError as ex:
                    pass

    def set_taskUpdateDate(self,timeStr=None):
        if timeStr == None:
            self.info["taskUpdateDate"] = datetime.now()
        elif type(timeStr) == datetime:
            self.info["taskUpdateDate"] = timeStr
        else:
            try:
                self.info["taskUpdateDate"] = datetime.strptime(timeStr,self.dateFormat)
            except ValueError as e:
                try:
                    self.info["taskUpdateDate"] = datetime.strptime(timeStr,self.altDateFormat)
                except ValueError as ex:
                    pass
            

    def set_taskCompleteDate(self,timeStr=None):
        self.status = "Done"
        if timeStr == None:
            self.info["taskCompleteDate"] = datetime.now()
        elif type(timeStr) == datetime:
            self.info["taskCompleteDate"] = timeStr
        else:
            try:
                self.info["taskCompleteDate"] = datetime.strptime(timeStr,self.dateFormat)
            except ValueError as e:
                try:
                    self.info["taskCompleteDate"] = datetime.strptime(timeStr,self.altDateFormat)
                except ValueError as ex:
                    pass
            

    def getAsJson(self):
        temp_record = {}
        for key in self.info:
            if type(self.info[key]) is datetime:
                temp_record[key] = self.info[key].strftime(self.dateFormat)
                
            else:
                temp_record[key] = self.info[key]
        retVal = json.dumps(temp_record) 

        return retVal
    
    def loadFromJson(self,value):
        valid_load = True
        try:
            local_record = json.loads(value)
            for key in local_record:
                if key in self.info:
                    if type(self.info[key]) is datetime:
                        self.info[key] = datetime.strptime(local_record[key],self.dateFormat)
                    else:
                        self.info[key] = local_record[key]
        except (json.JSONDecodeError, ValueError) as e:
            valid_load = False

        return valid_load
