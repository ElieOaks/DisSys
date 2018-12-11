import getpass
import pickle
import time

users = { 
'ilda' : 'mehic',
'johannes' : 'almroth',
'erik' : 'ohlsson',
'joy' : 'van den eijkhof'
}

answer= ""

def welcomeMenu():
    answer = input("\nWould u like to: \n *log in (press l) \n *quit(press q)\n")
    if answer == "l":
        user_login()
    elif answer == "q":
        quit()
    else:
        print ("\nWrong input, try again\n")
        welcomeMenu()

def user_login ():
    login = input ("Please enter your username:")
    password = getpass.getpass("Please enter your password:")
    if login in users and users[login] == password:
        print ("\nYou are successfully logged in\n")    
    else:
        print ("\nUsername or password incorrect\n")
        user_login()

welcomeMenu()




'''
def users_dictionary_load():
    try:
        with open("users.txt", "rb") as blah:
            blah.seek(0)
            return pickle.load(blah)
    except IOError:
        with open("users.txt", "w+") as blah:
            pickle.dump(dict(), blah)
            return dict()

def users_dictionary_save(dictAcc):
    with open("users.txt", "wb") as blah:
        pickle.dump(users, blah)

def register():
    dictAcc = users_dictionary_load()
    newUser = input ("\nEnter your username\n")
    if (newUser in dictAcc):
        print ("\nPlease choose another username \n")
        register()
    else:
        newPassword = getpass.getpass("\nPlease choose your password \n")
        if len(newPassword) < 4:
            print ("Your password must be at least 4 characters long. ")
            register() 
        else:
            dictAcc[newUser] = newPassword
            print ("\nYour user is now created, what would u like to do next? \n")
            users_dictionary_save(dictAcc)
            welcomeMenu()

'''
