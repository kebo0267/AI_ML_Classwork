from datetime import datetime, timedelta
import json

class TaskRecord:
    def __init__(self):
        self.record ={}
        self.record["taskId"] = int(0)
        self.record["userId"] = int(0)
        self.record["title"] = ""
        self.record["description"] = ""
        self.record["dueDate"] = datetime.now()
        self.record["createDate"] = datetime.now()
        self.record["startDate"] = datetime.now()
        self.record["completeData"] = datetime.now()
        self.dateFormat = "%Y-%m-%d %H:%M:%S"

    @property
    def taskId(self):
        return self.record["taskId"]
    
    @taskId.setter
    def taskId(self,new_taskId):
        self.record["taskId"] = new_taskId

    @property
    def userId(self):
        return self.record["userId"]
    
    @userId.setter
    def userId(self,new_userId):
        self.record["userId"] = new_userId

    @property
    def title(self):
        return self.record["title"]
    
    @title.setter
    def title(self,new_title):
        self.record["title"] = new_title

    @property
    def description(self):
        return self.record["description"]
    
    @description.setter
    def description(self,new_desc):
        self.record["description"] = new_desc

    @property
    def dueDate(self):
        return self.record["dueDate"]
    
    @dueDate.setter
    def dueDate(self,new_dueDate):
         self.record["dueDate"] = new_dueDate

    @property
    def createDate(self):
        return self.record["createDate"]
    
    @createDate.setter
    def createDate(self,new_createDate):
        self.record["createDate"] = new_createDate

    @property
    def startDate(self):
        return self.record["startDate"]
    
    @startDate.setter
    def startDate(self,new_startDate):
        self.record["startDate"] = new_startDate

    @property
    def completeData(self):
        return self.record["completeData"]
    
    @createDate.setter
    def completeData(self,new_completeData):
        self.record["completeData"] = new_completeData

    def saveAsJson(self):
        temp_record = {}
        for key in self.record:
            if type(self.record[key]) == datetime:
                temp_record[key] = self.record[key].strftime(self.dateFormat)
            else:
                temp_record[key] = self.record[key]

        return json.dumps(temp_record) 
    
    def loadJson(self,value):
        local_record = json.loads(value)
        for key in local_record:
            if key in self.record:
                if type(self.record[key]) == datetime:
                    self.record[key] = datetime.strptime(local_record[key],self.dateFormat)
            else:
                self.record[key] = local_record[key]
