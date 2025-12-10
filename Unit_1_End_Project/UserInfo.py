import base64
import json
from datetime import datetime, timedelta

class UserInfo:
    def __init__(self):
        self.info = {}
        self.info["userName"] = ""
        self.info["password"] = ""
        self.info["lastLogin"] = datetime.now()
        self.info["failedLogin"] = datetime.now()
        self.info["failedCount"] = 0
        self.maxFailedCount = 3
        self.logoutResetInterval = timedelta(minutes=15)
        self.dateFormat = "%Y-%m-%d %H:%M:%S"

    @property
    def userName(self):
        return self.info["userName"]
    
    @userName.setter
    def userName(self,new_userName):
        self.info["userName"] = new_userName

    @property
    def password(self):
        return self.info["password"]

    @password.setter
    def password(self,new_password):
        encoded_password = base64.b64encode(new_password.encode('utf-8'))
        self.info["password"] = str(encoded_password)

    @property
    def failedLoginCount(self):
        return self.info["failedCount"]
    
    @failedLoginCount.setter
    def failedLoginCount(self,new_count):
        self.info["failedCount"] = new_count

    @property
    def lastLoginTime(self):
        return self.info["lastLogin"]

    @property
    def lastFailedLoginTime(self):
        return self.info["failedLogin"]
    

    def set_pre_encoded_password(self, enc_password):
        self.info["password"] = enc_password

    def checkPassword(self, password):
        if self.failedLoginCount > self.maxFailedCount and ((datetime.now() - self.lastFailedLoginTime) < self.logoutResetInterval):
            retVal = False
        else:
            encoded_password = base64.b64encode(password.encode('utf-8'))
            retVal = str(encoded_password) == self.password

        if ((datetime.now() - self.lastFailedLoginTime) > self.logoutResetInterval):
            self.failedLoginCount = 0
        
        return retVal 
    

    def setLoginTime(self,timeStr=None):
        if timeStr == None:
            self.info["lastLogin"] = datetime.now()
        elif type(timeStr) == datetime:
            self.info["lastLogin"] = timeStr
        else:
            self.info["lastLogin"] = datetime.strptime(timeStr,self.dateFormat)

        self.failedLoginCount = 0
        

    def setFailedLoginTime(self,timeStr=None):
        if timeStr == None:
            self.info["failedLogin"] = datetime.now()
        elif type(timeStr) == datetime:
            self.info["failedLogin"] = timeStr
        else:
            self.info["failedLogin"] = datetime.strptime(timeStr,self.dateFormat)

        if self.failedLoginCount <= self.maxFailedCount:
            self.failedLoginCount += 1

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
