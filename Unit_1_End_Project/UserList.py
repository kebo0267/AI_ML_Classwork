import UserInfo
import string

class UserList:
    def __init__(self):
        self.userList = []
        self.nextUserId = 0
        self.userListFileName = "userList.jsonl"

    def addUser(self,userName,password):
        user = UserInfo.UserInfo()
        user.userId = self.nextUserId
        user.userName = userName
        user.password = password
        self.userList.append(user)
        self.nextUserId += 1
        self.saveRecords()

    def removeUser(self,userName):
        for index in range(0, len(self.userList)):
            if userName == self.userList[index].userName:
                self.userList.pop(index)
                break
        self.saveRecords()

    def getUser(self,userName):
        retVal = None
        for index in range(0, len(self.userList)):
            if userName == self.userList[index].userName:
                retVal = self.userList[index]
                break
        return retVal
    
    def updateUser(self,userName,password):
        for index in range(0, len(self.userList)):
            if userName == self.userList[index].userName:
                self.userList[index].password = password
                break
        self.saveRecords()

    def checkuUserExist(self,userName):
        retVal = False
        for index in range(0, len(self.userList)):
            if userName == self.userList[index].userName:
                retVal = True
                break
        return retVal
    
    def checkPasswordValid(self, password,comment=""):
        retVal = False
        specChar = string.punctuation
        if len(password) < 8:
            comment = "Password too short"
        elif not any(char.isupper() for char in password):
            comment = "Password must contain Uppercase Letters."
        elif not any(char.islower() for char in password):
            comment = "Password must contain Lowercase Letters."
        elif not any(char in specChar for char in password):
            comment = "Password must contain special characters."
        else:
            retVal = True

        return retVal
    
    def loginUser(self,userName,password):
        retVal = False
        for index in range(0, len(self.userList)):
            if userName == self.userList[index].userName:
                if not self.userList[index].checkPassword(password):
                    self.userList[index].setFailedLoginTime()
                else:
                    self.userList[index].setLoginTime()
                    retVal = True
                break
        self.saveRecords()
        return retVal

    
    def saveRecords(self):
        jFile = open(self.userListFileName,"w")
        for records in self.userList:
            print(records)
            outputStr = records.getAsJson()
            print(outputStr)
            jFile.write(outputStr)
            jFile.write("\n")
        jFile.close()

