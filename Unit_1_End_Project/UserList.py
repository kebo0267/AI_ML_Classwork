import UserInfo
import string
import os

class UserList:
    def __init__(self):
        self.userList = {}
        self.nextUserId = 0
        self.userListFileName = "userList.jsonl"

    def addUser(self,userName,password):
        print (f'Adding account {userName} with passord {password}')
        user = UserInfo.UserInfo()
        #user.userId = self.nextUserId
        #user.userId = len(self.userList)
        user.userName = userName
        user.password = password
        self.userList[userName] = user
        #self.nextUserId += 1
        self.saveRecords()

    def removeUser(self,userName):
        user = self.userList.pop(userName,None)
        if not user == None:
            self.saveRecords()

    def getUser(self,userName):
        retVal = self.userList.get(userName,None)
        return retVal
    
    def updateUser(self,userName,password):
        user = self.userList.get(userName,None)
        if not user == None:
            user.password = password
            self.saveRecords()

    def checkuUserExist(self,userName):
        retVal = userName in self.userList.keys()
        
        return retVal
    
    def checkPasswordValid(self, password,comment):
        retVal = False
        specChar = string.punctuation
        if len(comment) == 0:
            comment.append("")
        if len(password) < 8:
            comment[0] = "Password too short"
        elif not any(char.isupper() for char in password):
            comment[0] = "Password must contain Uppercase Letters."
        elif not any(char.islower() for char in password):
            comment[0] = "Password must contain Lowercase Letters."
        elif not any(char in specChar for char in password):
            comment[0] = "Password must contain special characters."
        else:
            retVal = True

        return retVal
    
    def loginUser(self,userName,password):
        retVal = False

        user = self.userList.get(userName,None)
        if not user == None:
            if not user.checkPassword(password):
                user.setFailedLoginTime()   
            else:
                user.setLoginTime()
                retVal = True
        
            self.saveRecords()
        return retVal

    
    def saveRecords(self):
        jFile = open(self.userListFileName,"w")
        for record in self.userList.values():
            outputStr = record.getAsJson()
            jFile.write(outputStr)
            jFile.write("\n")
        jFile.close()

    def loadRecords(self,userFileName=None):
        if not userFileName == None:
            self.userListFileName = userFileName
        if os.path.isfile(self.userListFileName):
            jFile = open(self.userListFileName,"r")
            userReords = jFile.readlines()
            print(len(userReords))
            for record in userReords:
                if len(record.strip()) > 0:
                    userInfo = UserInfo.UserInfo()
                    if userInfo.loadFromJson(record):
                        self.userList[userInfo.userName] = userInfo
                    print(record)
            jFile.close()

