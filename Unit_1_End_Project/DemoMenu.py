import os
import UserList
from IPython.display import clear_output

class DemoMenu:
    def __init__(self,userData=None):
        self.running = True
        self.userList = UserList.UserList()
        self.userList.loadReords(userData)


    def clear_console(self):
        if os.name == "nt":
            os.system('cls')
        else:
            clear_output()
            

    def login(self):
        menuOptions = ["User Name","Password"]
        loginStatus = False
        self.clear_console()
        
        print("Enter User Name")
        userName = input(f'{menuOptions[0]} : ')
        if len(userName) > 0:            
            print("Enter Password")
            password = input(f'{menuOptions[1]} : ')
            if (len(password) > 0):
                if self.userList.loginUser(userName,password):
                    print("Login Successful")
                    loginStatus = True
                else:
                    print("Login Failed")
            
        return loginStatus


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

                             

    def mainMenu(self):
        menuOptions = ["Sign In","Sign Up"]
        while self.running:
            self.clear_console()
            for optIndex in range(0,len(menuOptions)):
                print(f'[{optIndex}] - {menuOptions[optIndex]}')
            print(f'[E] - Exit')

            value = input("Choose Option: ") 

            if (value.upper() == "E") or len(value) == 0:
                self.clear_console()
                self.running = False
                break
            try:

                menuIndx = int(value)
                if menuIndx < 0 or menuIndx >= len(menuOptions):
                    continue
                
                if menuIndx == 0:
                    self.login()
                elif menuIndx == 1:
                    self.signup()
                else:
                    continue
            except ValueError:
                print("Invalid value entered.")
            
            
        

if __name__ == "__main__":
    menu = DemoMenu()
    menu.mainMenu()