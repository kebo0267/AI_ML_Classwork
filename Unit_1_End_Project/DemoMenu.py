import os
import UserList
import TaskList
import TaskInfo
from datetime import datetime, timedelta
from IPython.display import clear_output

class DemoMenu:
    def __init__(self,userData=None,taskData=None):
        self.running = True
        self.userList = UserList.UserList()
        self.userList.loadRecords(userData)
        self.taskList = TaskList.TaskList()
        self.taskList.loadRecords(taskData)


    def clear_console(self):
        print(os.name)
        clear_output()
        if os.name == "nt":
            os.system('cls')
        else:
            clear_output()
            

    def printMenu(self,menuOptions,comments="",showIndex=True):
        self.clear_console()
        print(comments)
        for optIndex in range(0,len(menuOptions)):
            if showIndex:
                print(f'[{optIndex}] - {menuOptions[optIndex]}')
            else:
                print(f'{menuOptions[optIndex]}')
        print(f'[E] - Exit')

    def login(self):
        menuOptions = ["User Name","Password"]
        loginUser = None
        self.clear_console()
        
        print("Enter User Name")
        userName = input(f'{menuOptions[0]} : ')
        if len(userName) > 0:            
            print("Enter Password")
            password = input(f'{menuOptions[1]} : ')
            if (len(password) > 0):
                if self.userList.loginUser(userName,password):
                    print("Login Successful")
                    loginUser = self.userList.getUser(userName)
                else:
                    print("Login Failed")
            
        return loginUser


    def signup(self):
        menuOptions = ["User Name","Password"]
        comment = [""]
        running = True
        
        while running:
            self.clear_console()
            print(comment[0])
            comment[0] = ""
            print("Create user name for acount.")
            userName = input(f'{menuOptions[0]} : ')
            if len(userName) < 1:
                running = False
                continue
            if self.userList.checkuUserExist(userName):
                comment[0] = f'User Name: {userName} exists.  Try another User Name.'
                continue
            else:
                print(f'User Name: {userName} is available.')
                print(f'Create password for user name {userName}')
            password = input(f'{menuOptions[1]} : ')
            if len(password) < 1:
                running = False
                continue
            if not self.userList.checkPasswordValid(password,comment):
                comment[0] = f'Invalid Password: {comment[0]}'
                continue
            else:
                print(f'Account for User {userName} created.')


            self.userList.addUser(userName,password)
            running = False


    def viewTasks(self):
        tasklist = list(self.taskList.getTaskList().values())
        self.clear_console()
        for task in tasklist:
            startdate = task.taskCreateDate.strftime(task.getDateTimeFormat())
            updatedate = task.taskUpdateDate.strftime(task.getDateTimeFormat())
            completdate = task.taskCompleteDate.strftime(task.getDateTimeFormat())
            outputStr = f'{task.taskId} - {task.taskName} - {task.status}'
            outputStr = f'{outputStr} {startdate} {updatedate} {completdate}'
            print(outputStr)

        print()
        print("Press Enter to continue.")
        value = input("Press any Key to return")
        
    def addTask(self,user):
        retVal = False
        menuOptions = ["Task Name", "Description","Due Date (yyyy-mm-dd)"]
        self.clear_console()
        print("Create a new task:")
        print(f'{menuOptions[0]} : ')
        taskName = input(f'{menuOptions[0]} : ')
        if len(taskName) < 1:
            return retVal
        
        print(f'{menuOptions[1]} : ')
        description = input(f'{menuOptions[1]} : ')
        
        print(f'{menuOptions[2]} : ')
        dueDateStr = input(f'{menuOptions[2]} : ')
        if len(dueDateStr) < 1:
            dueDateStr = None
        
        task = TaskInfo.TaskInfo()
        task.taskName = taskName
        task.description = description
        task.taskCreateDate(dueDateStr)
        task.createUser = user.userName
        self.taskList.addTask(task)
        
    def updateTask(self):
        self.clear_console()
        print("Complete Task")
        print("Task ID  -  Task Name")
        taskList = list(self.taskList.getTaskList().values())
        for task in taskList:
            print(f'{task.taskId} - {task.taskName}')
        
        print(f'[E] - Exit')
        print() 
        print(f'Select Task ID : ')
        value = input(f'Task ID : ')
        if (value.upper() == "E") or len(value) == 0:
            self.clear_console()
            return
        
        taskId = int(value)
        if taskId < 0 or taskId >= len(taskList):
            return
        
        task = self.taskList.getTask(taskId)
        if task == None:
            return
        
        task.taskCompleteDate()
        self.taskList.updateTask(task) 
        



    def removeTask(self):
        self.clear_console()
        print("Remove Task")
        print("Task ID  -  Task Name")
        taskList = self.taskList.getTaskList().values()
        for task in taskList:
            print(f'{task.taskId} - {task.taskName}')
        
        print(f'[E] - Exit')

        print()
        print(f'Select Task ID : ')
        value = input(f'Task ID : ')
        if (value.upper() == "E") or len(value) == 0:
            self.clear_console()
            return
        
        taskId = int(value)
        if taskId < 0 or taskId >= len(taskList):
            return
        
        task = self.taskList.removeTask(taskId)

    def taskingMenu(self,user=None):
        running = True
        if user == None:
            return
        menuOptions = ["View Tasks","Add Task","Complete Task", "Remove Task"]
        while running:
            userNameStr = f' User {user.userName}'
            self.printMenu(menuOptions,userNameStr)
            print()
            value = input("Choose Option: ") 
            if (value.upper() == "E") or len(value) == 0:
                self.clear_console()
                running = False
                break

            try:
                menuIndex = int(value)

                if menuIndex < 0 or menuIndex >= len(menuOptions):
                    comment = "Invalid value entered."
                    continue
                elif menuIndex == 0:
                    self.viewTasks()
                elif menuIndex == 1:
                    self.addTask(user)
                elif menuIndex == 2:
                    self.updateTask()
                elif menuIndex == 3:
                    self.removeTask()
            except ValueError:
                print("Invalid value entered.")


    def mainMenu(self):
        menuOptions = ["Sign In","Sign Up"]
        comment = ""
        while self.running:
            
            self.printMenu(menuOptions,comment)
            
            value = input("Choose Option: ") 

            if (value.upper() == "E") or len(value) == 0:
                self.clear_console()
                self.running = False
                break
            try:
                menuIndx = int(value)
                if menuIndx < 0 or menuIndx >= len(menuOptions):
                    comment = "Invalid value entered."
                    continue
                
                if menuIndx == 0:
                    userInfo = self.login()
                    if  userInfo != None:
                        self.taskingMenu(userInfo)
                    else:
                        comment = "Login Failed."
                elif menuIndx == 1:
                    self.signup()
                else:
                    continue
            except ValueError:
                print("Invalid value entered.")
            
            
        

if __name__ == "__main__":
    menu = DemoMenu()
    menu.mainMenu()