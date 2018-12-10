import getpass

users = { 
'ilda' : 'mehic',
'johannes' : 'almroth',
'erik' : 'ohlsson',
'joy' : 'van den Eijkhof'
}

answer= ""

def welcomeMenu():
    answer = raw_input("\nWould u like to: \n *log in (press l) \n *quit(press q)\n")
    if answer == "l":
        user_login()
    elif answer == "q":
        quit()
    else:
        print ("\nWrong input, try again\n")
        welcomeMenu()

def user_login ():
    login = raw_input ("Please enter your username:")
    password = getpass.getpass("Please enter your password:")
    if login in users and users[login] == password:
        print ("\nYou are successfully logged in\n")    
    else:
        print ("\nUsername or password incorrect\n")
        user_login()

welcomeMenu()

'''
def register():
    newUser = raw_input ("\nEnter your username\n")
    if newUser in users:
        print ("\nildPlease choose another username \n")
        register()
    else:
        newPassword = getpass.getpass("\nPlease choose your password \n")
        if len(newPassword) < 4:
            print ("Your password must be at least 4 characters long. ")
            register() 
        else:
            newUser == newPassword and users["newUser"] == "newPassword" 
            print ("\nYour user is now created, what would u like to do next? \n")
            welcomeMenu()
'''

