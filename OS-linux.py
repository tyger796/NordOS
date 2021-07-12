## Packages
import time
import sys
import random
import os
from os import path
from datetime import date
from cryptography.fernet import Fernet
import shutil
import getpass

def slowprint(s):
  for c in s + '\n':
    sys.stdout.write(c)
    sys.stdout.flush()
    time.sleep(1./10)

def clear():
    os.system('clear')

## main
clear()
slowprint("Booting OS...")
time.sleep(3)
clear()

## Data directory
if os.path.isdir("./data"):
    print("[Debug] Found 'data' directory.")
else:
    dir = "data"
    parent = "./"
    path = os.path.join(parent, dir)
    os.mkdir(path)
    print("[Debug] Couldn't find 'data' directory, creating one...")

## Key gen
if os.path.isfile("./data/.mykey.key"):
  print("[Debug] Found encryption key!")
else:
  print("[Debug] Couldn't find encryption key, generating one...")
  key = Fernet.generate_key()
  with open('mykey.key', 'wb') as mykey:
    mykey.write(key)
  shutil.move("./mykey.key", "./data/mykey.key")
  os.system("mv ./data/mykey.key ./data/.mykey.key")

## Profile
if os.path.isdir("./profiles"):
  print("[Debug] Found the profiles directory!")
else:
  print("[Debug] Couldn't find the profiles directory, creating one...")
  dir = "profiles"
  parent = "./"
  path = os.path.join(parent, dir)
  os.mkdir(path)

## ask for username and password
passwordCHECKS = True
while passwordCHECKS == True:
  username = input("Username: ")
  password = getpass.getpass()

  ## check if the profile directory exists
  profilePath = ("./profiles/" + username)
  if os.path.isdir(profilePath):
    print("[Debug] Found profile!")
    passwordPATH = profilePath + "/password.txt"
    f = open(passwordPATH)
    encryptedPASSWORD = bytes(f.read(), encoding='utf8')
    f.close()
    f = open("./data/.mykey.key")
    key = f.read()
    f.close()
    f = Fernet(key)
    decryptedPASSWORD = f.decrypt(encryptedPASSWORD)
    decryptedPASSWORD = decryptedPASSWORD.decode("utf-8")
    decryptedPASSWORD = decryptedPASSWORD.replace("b" , "")
    decryptedPASSWORD = decryptedPASSWORD.replace("'", "")
    if decryptedPASSWORD == password:
      print("Password correct!")
      passwordCHECKS = False
    else:
      print("The password is incorrect, please try again.")


  ## no profile directory
  else:
    print("[Debug] Profile not found, creating one...")
    parent = "./profiles"
    path = os.path.join(parent, username)
    os.mkdir(path)
    ## create the username txt file
    f = open("username.txt", "xt")
    f.write(username)
    f.close()
    ## move txt file
    shutil.move("./username.txt", "./profiles/" + username + "/username.txt")
    ## open key and store it
    file = open('./data/.mykey.key', "rb")
    key = file.read()
    file.close()
    ## encrypt password
    password = password.encode()
    f = Fernet(key)
    encrypted = f.encrypt(password)
    ## create encrypted password txt
    f = open("password.txt", "xb")
    f.write(encrypted)
    f.close()
    ## move the password file to profile directory
    shutil.move("./password.txt", "./profiles/" + username + "/password.txt")
    print("Successfully Created profile, " + username)
    time.sleep(3)
    clear()
    passwordCHECKS = False
  
print("Welcome " + username)
slowprint("Loading...")
time.sleep(2)
clear()
logo1 = str("▒█▄░▒█ █▀▀█ █▀▀█ █▀▀▄ ▒█▀▀▀█ ▒█▀▀▀█")
logo2 = str("▒█▒█▒█ █░░█ █▄▄▀ █░░█ ▒█░░▒█ ░▀▀▀▄▄")
logo3 = str("▒█░░▀█ ▀▀▀▀ ▀░▀▀ ▀▀▀░ ▒█▄▄▄█ ▒█▄▄▄█")
print(logo1)
print(logo2)
print(logo3)
print("NordOS Version 1.0")
today = date.today()
d2 = today.strftime("%B %d, %Y")
print("[" + d2 + "]")
print("Logged in as", username)
commandInput = True
command = input(username + "@NORD_OS:~$ ")
while commandInput == True:
## help
  if command == "help":
    slowprint("Welcome to...")
    print(logo1)
    print(logo2)
    print(logo3)
    print("\n")
    slowprint("To find some commands, use 'commands' in the shell.")
    command = input(username + "@NORD_OS:~$ ")
## commands
  elif command == "commands":
    print("\nCommands")
    print("-------------")
    print("help - Sends a help message to get you started!")
    print("commands - You're here!")
    print("exit - Closes NordOS.")
    print("-------------\n")
    command = input(username + "@NORD_OS:~$ ")
##exit command
  elif command == "exit":
    exiting = True
    while exiting == True:
      passwordINPUT = getpass.getpass()
      if passwordINPUT == decryptedPASSWORD:
        slowprint("Closing... see you soon :)")
        time.sleep(3)
        commandInput = False
        exiting = False
        exit()
      else:
        print("The password given was incorrect, please try again.")
  elif command == "":
    slowprint("Please type a command and press enter, for help type 'help' and press enter.")
    command = input(username + "@NORD_OS:~$ ")
  else:
    slowprint("Command not found!")
    command = input(username + "@NORD_OS:~$ ")
exit()
