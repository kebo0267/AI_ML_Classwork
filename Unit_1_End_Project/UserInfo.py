import base64
import json
from datetime import datetime, timedelta

class UserInfo:
    def __init__(self):
        self.info = {}
        self.info["userId"] = ""
        self.info["userName"] = ""
        self.info["password"] = ""
        self.info["lastLogin"] = None
        self.info["failedLogin"] = None
        self.info["failedCount"] = 0
        self.dateFormat = "%Y-%m-%d %H:%M:%S"

    @property
    def userId(self):
        return self.info["userId"]
    
    @userId.setter
    def userId(self,new_userId):
        self.info["userId"] = new_userId

    @property
    def userName(self):
        return self.userName["userName"]
    
    @userName.setter
    def userName(self,new_userName):
        self.info["userName"] = new_userName

    @property
    def password(self):
        return self.info["password"]

    @password.setter
    def password(self,new_password):
        self.info["password"] = new_password.encode('utf-8')

    def checkPassword(self, password):
        return password.encode('utf-8') == self.info["password"]

    def setLoginTime(self,timeStr=None):
        if timeStr == None:
            self.info["lastLogin"] = datetime.now()
        elif type(timeStr) == datetime:
            self.info["lastLogin"] = timeStr
        else:
            self.info["lastLogin"] = datetime.strptime(timeStr,self.dateFormat)

        self.info["failedCount"] = 0

    def setFailedLoginTime(self,timeStr=None):
        if timeStr == None:
            self.info["failedLogin"] = datetime.now()
        elif type(timeStr) == datetime:
            self.info["failedLogin"] = timeStr
        else:
            self.info["failedLogin"] = datetime.strptime(timeStr,self.dateFormat)

        self.info["failedCount"] += 1

    def getAsJson(self):
        temp_record = {}
        for key in self.info:
            print(key)
            if type(self.info[key]) == datetime:
                temp_record[key] = self.info[key].strftime(self.dateFormat)
            else:
                temp_record[key] = self.info[key]

        return json.dumps(temp_record) 
    
    def loadFromJson(self,value):
        local_record = json.loads(value)
        for key in local_record:
            if key in self.info:
                if type(self.info[key]) == datetime:
                    self.info[key] = datetime.strptime(local_record[key],self.dateFormat)
                else:
                    self.info[key] = local_record[key]
