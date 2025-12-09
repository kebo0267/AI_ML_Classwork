import os
import UserList
from IPython.display import clear_output

class DemoMenu:
    def __init__(self):
        self.running = True
        self.userList = UserList.UserList()

    def clear_console(self):
        if os.name == "nt":
            os.system('cls')
        else:
            clear_output()
            

    def pick_login(self):
        menuOptions = ["User Name","Password"]
        comment = ""
        while self.running:
            self.clear_console()
            print(comment)
            userName = input(f'{menuOptions[0]} : ')
            password = input(f'{menuOptions[1]} : ')
            if self.userList.loginUser(userName,password):
                pass
            
            break

    def pick_signup(self):
        menuOptions = ["User Name","Password"]
        
        comment = ""
        while self.running:
            self.clear_console()
            print(comment)
            userName = input(f'{menuOptions[0]} : ')
            password = input(f'{menuOptions[1]} : ')
            
            if self.userList.checkuUserExist(userName):
                print(f'User Name: {userName} exist.  Try another User Name.')
                continue

            if not self.userList.checkPasswordValid(password,comment):
                print(f'Invalid Password: {comment}')
                continue
            self.userList.addUser(userName,password)
            break

                             

    def mainMenu(self):
        menuOptions = ["Sign In","Sign Up"]
        while self.running:
            self.clear_console()
            for optIndex in range(0,len(menuOptions)):
                print(f'[{optIndex}] - {menuOptions[optIndex]}')
            print(f'[E] - Exit')

            value = input("Choose Option: ") 
            if value.upper() == "E":
                self.clear_console()
                self.running = False
                break
            try:

                menuIndx = int(value)
                if menuIndx < 0 or menuIndx >= len(menuOptions):
                    continue
                
                if menuIndx == 0:
                    self.pick_login()
                elif menuIndx == 1:
                    self.pick_signup()
                else:
                    continue
            except ValueError:
                print("Invalid value entered.")
            
            
        

if __name__ == "__main__":
    menu = DemoMenu()
    menu.mainMenu()