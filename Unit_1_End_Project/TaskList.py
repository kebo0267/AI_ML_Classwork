import TaskInfo
import string
import os

class TaskList:
    def __init__(self):
        self.taskList = {}
        self.nextUserId = 0
        self.taskListFileName = "TaskList.jsonl"

    def addTask(self,taskInfo):
        taskInfo.taskId = len(self.taskList)
        self.taskList[taskInfo.taskId] = taskInfo
        
        self.saveRecords()

    def removeTask(self,taskId):
        task = self.taskList.pop(taskId,None)
        if not task == None:
            self.saveRecords()
        return task

    def getTask(self,taskId):
        retVal = self.taskList.get(taskId,None)
        return retVal
    
    def getTaskList(self):
        return self.taskList

    def getListofTaskNames(self):
        retVal = []

        for key in self.taskList.keys():
            retVal.append(self.taskList[key].taskName)
        return retVal
        
    
    def updateTask(self,task):
        self.taskList[task.taskId] = task
        self.saveRecords()

    def checkTaskExists(self,taskId):
        retVal = taskId in self.taskList.keys()
        
        return retVal
      
    
    def saveRecords(self):
        jFile = open(self.taskListFileName,"w")
        for record in self.taskList.values():
            outputStr = record.getAsJson()
            print(outputStr)
            jFile.write(outputStr)
            jFile.write("\n")
        jFile.close()

    def loadRecords(self,taskFileName=None):
        if not taskFileName == None:
            self.taskListFileName = taskFileName
        if os.path.isfile(self.taskListFileName):
            jFile = open(self.taskListFileName,"r")
            taskReords = jFile.readlines()
            
            for record in taskReords:
                if len(record.strip()) > 0:
                    taskInfo = TaskInfo.TaskInfo()
                    if taskInfo.loadFromJson(record):
                        self.taskList[taskInfo.taskId] = taskInfo
                    print(record)
            jFile.close()

