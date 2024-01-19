print("Starting systems...")
try:
  from numpy import random as rn
  import random
  import string
  import pygsheets
  import re
  from hashlib import sha256
  from google.oauth2 import service_account
  import json 
  import requests

  print("Authorizing user...")

  # authorize the clientsheet 

  SCOPES = ('https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive')
  data = json.loads(requests.get('URL HIDDEN').text)
  client = pygsheets.authorize(custom_credentials=service_account.Credentials.from_service_account_info(data, scopes=SCOPES))

  #get the instance of the Spreadsheet
  sheet = client.open('data test')

  print("Gathering data...")

  # get the first sheet of the Spreadsheet
  sheet_instance = sheet.worksheet_by_title('Sheet1')
  sheet_hash = sheet.worksheet_by_title('hash')

  records_data = sheet_instance.get_all_records()
  hash_data = sheet_hash.get_all_records()
except Exception as e:
  print("Something went wrong, shutting down systems...")
  print("Please try again later...")
  print(e)
  exit()
# sign in

signin = True
print("(Type 'no' if you wish to sign up)")
signedin = input("Would you like to sign in? ")
if "y" in signedin.lower():
  print("Starting up...")
elif "n" in signedin.lower():
  signedin = input("Would you like to sign up? ")
  if "y" in signedin.lower():
    signin = False
    print("Starting signup...")
  elif "n" in signedin.lower():
    print("Exiting solution...")
    exit()
  else:
    print("Unknown command... Exiting solution...")
    exit()
else:
  print("Unknown command... Exiting solution...")
  exit()

def checkUsername(username):
  if len(sheet_instance.find(username, searchByRegex=False, matchCase=True, 
     matchEntireCell=False, includeFormulas=False, 
    cols=(1,(sheet_instance.rows + 1)), rows=None, forceFetch=True)) != 0:
    return True
  else:
    return False

def checkDuplicate(search, col):
  if len(sheet_instance.find(search, searchByRegex=False, matchCase=True, 
     matchEntireCell=False, includeFormulas=False, 
    cols=(col,(sheet_instance.rows + 1)), rows=None, forceFetch=True)) != 0:
    return True
  else:
    return False

def bold(text):
  return ("\033[1m" + text + "\033[0m")

def italic(text):
  return ("\033[3m" + text + "\033[0m")

def search(lists, string):
  for i in lists:
    if string == i:
      return True
  return False

if signin == True:
  while True:
    username = input("Please type in your username: ")
    if username != "username" and checkUsername(username) == True:
      print(f"Hi, {username}!")
      passwordR = next((item for item in hash_data if item["username"] == username), None)
      passwordR = passwordR["hash"]
      break
    else: 
      print("Invalid username... Please try again!")
  password = input("Now please type in your password: ")
  while True:
    if sha256(password.encode('utf-8')).hexdigest() == passwordR:
      print(f"Welcome back, {username}!")
      break
    else:
      print("Wrong password!")
      password = input(f"Please retype the password for {username}: ")
else:
  while True:
    username = input("Please type in your new username: ")
    if len(username) > 3 and username.lower() != "username" and username[0] != "=" and username[0] != '+':
      if not any(d['username'] == username for d in records_data):
        print(f"Username valid. Welcome, {username}")
        break
      else:
        print("Username already taken, please try again.")
    else:
      print("Username has to be more than 3 characters long" if len(username) < 3 else "This is an invalid username, please choose something else")
  while True:
    password = input("Please create your new password: ")
    if len(password) > 3 and password.lower() != "password":
      print("Password valid. Creating new account...")
      break
    else:
      print("Your password must be longer than 3 characters..." if len(password) < 3 else "You cannot set your password to 'password'")
  sheet_hash.add_rows(1)
  sheet_hash.update_row(sheet_hash.rows, [[username,sha256(password.encode('utf-8')).hexdigest()]])
  salt = ''.join(random.choice(string.ascii_letters+string.digits+string.punctuation) for i in range(16))
  while checkDuplicate(salt, 7) == True and salt[0] != "=" and salt[0] != "+":
    salt = ''.join(random.choice(string.ascii_letters+string.digits+string.punctuation) for i in range(16))
  sheet_instance.add_rows(1)
  sheet_instance.update_row(sheet_instance.rows, [[username,500,0,"user",salt]])
  print(f"Congratulations, {username}, you have officially set up your new account!")
  print("The console will close, so you will have to sign in once again")
  quit()

location = next((item for item in records_data if item["username"] == username), None)

if location["salt"] == "":
  print("Generating Salt...")
  salt = ''.join(random.choice(string.ascii_letters+string.digits+">?@[\]^_`{|}~,-./:;<!#$%&'()*") for i in range(16))
  while checkDuplicate(salt, 7) == True:
    salt = ''.join(random.choice(string.ascii_letters+string.digits+">?@[\]^_`{|}~,-./:;<!#$%&'()*") for i in range(16))
  sheet_instance.update_row(((next((i for i, item in enumerate(records_data) if item["username"] == username), None) + 2)), [[salt]], col_offset=4)
  print("Securing Password...")
  sheet_hash.add_rows(1)
  sheet_hash.update_row(sheet_hash.rows, [[username,sha256(password.encode('utf-8')).hexdigest()]])

while True:
  if location["rank"] == "mute":
    print(f"\nUnfortunately, you've been muted by either the owner or a moderator.\nAll this means, is that you've been suspected of doing something wrong, and you will be returned to normal after the moderators/owners decide so\nIf you feel they have mistaken you for doing something wrong, then please contact the owner.\nThank you for cooperating \n - {bold('OWNER')} \n ")
    break
  userInput = input("Please type in a command: ").lower()
  userInput = userInput.replace(" ", "")
  print("")
  if userInput == "help":
    helpList = {"Help" : "Shows a list of all the available commands",
    "Bal" : "Shows your current bank balance", 
    "Work" : "Allows you to play a simple minigame for money ", 
    "Dep" : "Allows you to deposit money into the bank (specified after typing command)", 
    "With" : "Allows you to withdraw money from the bank (specified after typing command)",
    "Rank" : "Shows your current rank",
    "Settings" : "Shows the currently available settings",
    "Exit" : "Exits the system"}
    print("Here's a list of commands: ")
    for i in helpList:
      print(bold(i) + " - " + italic(helpList[i]))
    if location["rank"] == "owner":
      print("\nHere's a list of ADMIN commands: ")
      ownerHelpList = { "Users" : "Shows a list of all the user account names",
      "Del" : "Deletes a user",
      "Add" : "Adds money to an account",
      "Sub" : "Removes money from an account",
      "Mute" : "Mutes a user",
      "Unmute" : "Unmutes a user",
      "UserInfo" : "Shows a list of information for a specific user",
      "UserRank" : "Grants a rank to a user"
      }
      for i in ownerHelpList:
        print(bold(i) + " - " + italic(ownerHelpList[i]))

      print("\nHere's a list of TESTER commands: ")
      testHelpList = { "SeeHash" : "Show what the hash value for a specific word would be",
      "CreateAcc" : "Create a new account"
      }
      for i in testHelpList:
        print(bold(i) + " - " + italic(testHelpList[i]))

      print("\nHere's a list of MODERATOR commands: ")
      modHelpList = { "Users" : "Shows a list of all the user account names",
      "Mute" : "Mutes a non-owner user",
      "Unmute" : "Unmutes a user",
      "UserInfo" : "Shows a list of information for a specific user"
      }
      for i in modHelpList:
        print(bold(i) + " - " + italic(modHelpList[i]))
    elif location["rank"] == "mod":
      print("\nHere's a list of MODERATOR commands: ")
      modHelpList = { "Users" : "Shows a list of all the user account names",
      "Mute" : "Mutes a non-owner user",
      "Unmute" : "Unmutes a user",
      "UserInfo" : "Shows a list of information for a specific user"
      }
      for i in modHelpList:
        print(bold(i) + " - " + italic(modHelpList[i]))
    print("\n")
  elif userInput == "bal":
    balance = next((item for item in records_data if item["username"] == username), None)
    balance = balance["balance"]
    bank = next((item for item in records_data if item["username"] == username), None)
    bank = bank["bank"]
    print(f'Your current balance: {bold(str(balance))}\nYour current bank balance: {bold(str(bank))}\n')
  elif userInput == "work":
    hint = rn.randint(1,100)
    hidden = rn.randint(1,100)
    print(f"I have picked two random numbers in the range 1-100.\nYour {bold('hint')} is {str(hint)}.\nYou must choose if the {bold('hidden number')} one of the following: \nA) The hint is {bold('lower')} than the hidden number\nB) The hint is {bold('higher')} than the hidden number\nC) The hint is {bold('equal')} to the hidden number")
    userGuess = re.sub("[^a,b,c]", "", input("Please type in the letter you choose: ").lower())
    userGuess = userGuess[:-(len(userGuess)-1)] if len(userGuess) > 1 else userGuess
    win = False
    if userGuess == "a":
      win = False if hint < hidden else True
    elif userGuess == "b":
      win = False if hint > hidden else True
    elif userGuess == "c":
      win = False if hint == hidden else True
    else:
      print("That is not a correct input... \nTherefore,")
    
    if win == True:
      print(f"Congratulations! You win! The hidden number was {str(hidden)}! 100 will be added to your balance!\n")
      balance = location["balance"]
      balance = int(balance) + 100
      sheet_instance.update_row(((next((i for i, item in enumerate(records_data) if item["username"] == username), None) + 2)), [[balance]], col_offset=1)
    else:
      print(f"You lose... The hidden number was {str(hidden)}. Good luck next time!\n")
  elif userInput == "dep":
    userInput = re.sub("[^0-9]", "", input("How much would you like to deposit? "))
    bank = next((item for item in records_data if item["username"] == username), None)
    bank = int(bank["bank"])
    balance = next((item for item in records_data if item["username"] == username), None)
    balance = int(balance["balance"])
    while True:
      if userInput == "":
        print("You cannot deposit nothing.\n")
        break
      else:
        userInput = int(userInput)
      if userInput < int(balance) or userInput == int(balance):
        print("Depositing...")
        bank = bank + userInput
        balance = balance - userInput
        sheet_instance.update_row(((next((i for i, item in enumerate(records_data) if item["username"] == username), None) + 2)), [[balance,bank]], col_offset=1)
        print(f"Deposited.\nYou now have {bold(str(bank))} in the bank, and {bold(str(balance))} as your current balance \n")
        break
      else:
        print("You cannot deposit more than you have\n")
        break
  elif userInput == "with":
    userInput = re.sub("[^0-9]", "", input("How much would you like to withdraw? "))
    bank = next((item for item in records_data if item["username"] == username), None)
    bank = int(bank["bank"])
    balance = next((item for item in records_data if item["username"] == username), None)
    balance = int(balance["balance"])
    while True:
      if userInput == "":
        print("You cannot withdraw nothing.\n")
        break
      else:
        userInput = int(userInput)
      if userInput < int(bank) or userInput == int(bank):
        print("Withdrawing...")
        bank = bank - userInput
        balance = balance + userInput
        sheet_instance.update_row(((next((i for i, item in enumerate(records_data) if item["username"] == username), None) + 2)), [[balance,bank]], col_offset=1)
        print(f"Withdrew.\nYou now have {bold(str(bank))} in the bank, and {bold(str(balance))} as your current balance \n")
        break
      else:
        print("You cannot deposit more than you have\n")
        break
  elif userInput == "rank":
    rank = location["rank"]
    print(f"Your rank is: {bold(rank.upper())} \nA rank is basically your status, for example the owner rank gives you full access to admin commands, while moderator allows you to mute users")
  elif userInput == "settings":
    print("Available Settings: ")
    settings = {
      "Username" : username,
      "Password" : "-------"
    }
    for i in range(len(settings)):print(f"{str(i+1)}) {str(list(settings.keys())[i])} : {str(list(settings.values())[i])}")
    userInput = int(re.sub("[^0-9]","",input("Please select a setting you would like to change: ")))
    if userInput == 1:
      while True:
        if sha256(input("Please verify yourself by retyping your password: ").encode('utf-8')).hexdigest() == password:
          print("Correct password!")
          break
        else:
          print("Wrong password - Please try again!")
      while True:
        usernameNew = input("Please type in your new username: ")
        if usernameNew != "username" and checkUsername(usernameNew) == True:
          print("Changing username...")
          sheet_instance.update_row(((next((i for i, item in enumerate(records_data) if item["username"] == username), None) + 2)), [[usernameNew]])
          username = usernameNew
          print(f"You changed your username to {username}!\n")
          break
    else: 
      print("Invalid username... Please try again!")
  elif userInput == "exit" or "exit" in userInput:
    print(f"Bye!\n - {bold('OWNER')} \n")
    break

  # MODERATOR COMMANDS
  elif (userInput == "users") and (location["rank"] == "mod" or location["rank"] == "owner"):
    print("Here's a list of users:")
    for i in records_data: print(bold(i["username"]))
    print("")
  elif (userInput == "mute") and (location["rank"] == "mod" or location["rank"] == "owner"):
    users = []
    userInput = input("Who would you like to mute? ")
    user = ""
    for i in records_data:
      if userInput == i["username"]:
        user = i["username"]
        break
    userInfo = next((item for item in records_data if item["username"] == user), None)
    if user == "":
      print("You cannot mute a user that doesn't exist!\n")
    elif userInfo["rank"] != "owner" and userInfo["rank"] != "mute" and user != username:
      print("Muting...")
      sheet_instance.update_row(((next((i for i, item in enumerate(records_data) if item["username"] == user), None) + 2)), [["mute"]], col_offset=3)
      print(f"{user} has been muted!\n")
    else:
      print("You cannot mute this person for the following reasons:\na) They either have the 'owner' rank\nb) Or they are already muted\nc) Or you accidentally attempted to mute yourself\n")
  elif (userInput == "unmute") and (location["rank"] == "mod" or location["rank"] == "owner"):
    users = []
    userInput = input("Who would you like to unmute? ")
    user = ""
    for i in records_data:
      if userInput == i["username"]:
        user = i["username"]
        break
    userInfo = next((item for item in records_data if item["username"] == user), None)
    if user == "":
      print("You cannot unmute a user that doesn't exist!\n")
    elif userInfo["rank"] != "owner" and userInfo["rank"] == "mute" and user != username:
      print("Unmuting...")
      sheet_instance.update_row(((next((i for i, item in enumerate(records_data) if item["username"] == user), None) + 2)), [["user"]], col_offset=3)
      print(f"{user} has been unmuted!\n")
    else:
      print("You cannot unmute someone who isn't muted!\n")
  elif (userInput == "userinfo") and (location["rank"] == "mod" or location["rank"] == "owner"):
    userInput = input("Who would you like information on? ")
    user = ""
    for i in records_data:
      if userInput == i["username"]:
        user = i["username"]
        break
    userInfo = next((item for item in records_data if item["username"] == user), None)
    if user == "":
      print("You cannot find information on a user that doesn't exist!")
    else:
      print(f"{bold(str(userInfo['username']))}'s information:")
      print(bold("USERNAME: ") + italic(userInfo["username"]))
      print(bold("BALANCE: ") + italic(str(userInfo["balance"])))
      print(bold("BANK AMOUNT: ") + italic(str(userInfo["bank"])))
      print(bold("RANK: ") + italic(userInfo["rank"]))
    print("")

  # OWNER COMMANDS
  elif userInput == "userrank" and location["rank"] == "owner":
    userInput = input("Who would you like to rank? ")
    user = ""
    for i in records_data:
      if userInput == i["username"]:
        user = i["username"]
        break
    userInfo = next((item for item in records_data if item["username"] == user), None)
    if user == "":
      print("You cannot rank a user that doesn't exist!\n")
    else:
      userInput = input("What rank would you like to give them? ").replace(" ","").lower()
      if userInput == "user" or userInput == "mod" or userInput == "mute" or userInput == "owner":
        print("Ranking...")
        sheet_instance.update_row(((next((i for i, item in enumerate(records_data) if item["username"] == user), None) + 2)), [[userInput]], col_offset=3)
        print("User ranked!\n")
      else:
        print("This is not a rank... \n")
  elif userInput == "del" and location["rank"] == "owner":
    userInput = input("Who's account would you like to delete? ")
    user = ""
    for i in records_data:
      if userInput == i["username"]:
        user = i["username"]
        break
    userInfo = next((item for item in records_data if item["username"] == user), None)
    if user == "":
      print("You cannot delete a user that doesn't exist!\n")
    elif user == username:
      print("You cannot delete yourself!\n")
    else:
      if "y" in input(f"{bold('You cannot undo this action!')}\nAre you sure? "):
        sheet_instance.delete_rows(((next((i for i, item in enumerate(records_data) if item["username"] == user), None) + 2)), number=1)
        sheet_hash.delete_rows(((next((i for i, item in enumerate(hash_data) if item["username"] == user), None) + 2)), number=1)
        print(f"{user} has been deleted!\n")
      else:
        print("Unknown response... Command terminated.\n")
  elif userInput == "add" and location["rank"] == "owner":
    userInput = input("Who's account would you like to add money to? ")
    user = ""
    for i in records_data:
      if userInput == i["username"]:
        user = i["username"]
        break
    userInfo = next((item for item in records_data if item["username"] == user), None)
    if user == "":
      print("You cannot select a user that doesn't exist!\n")
    else:
      userInput = int(re.sub("[^0-9]", "", input("How much money would you like to add? ")))
      balance = userInfo["balance"]
      balance = int(balance) + userInput
      sheet_instance.update_row(((next((i for i, item in enumerate(records_data) if item["username"] == user), None) + 2)), [[balance]], col_offset=1)
      print(f"Added {str(userInput)} to {user}!\n")
  elif userInput == "sub" and location["rank"] == "owner":
    userInput = input("Who's account would you like to remove money from? ")
    user = ""
    for i in records_data:
      if userInput == i["username"]:
        user = i["username"]
        break
    userInfo = next((item for item in records_data if item["username"] == user), None)
    if user == "":
      print("You cannot select a user that doesn't exist!\n")
    else:
      userInput = int(re.sub("[^0-9]", "", input("How much money would you like to remove? ")))
      balance = userInfo["balance"]
      balance = userInput - int(balance)
      sheet_instance.update_row(((next((i for i, item in enumerate(records_data) if item["username"] == user), None) + 2)), [[balance]], col_offset=1)
      print(f"Removed {str(userInput)} from {user}!\n")

  # TESTER COMMANDS
  elif userInput == "seehash" and location["rank"] == "owner":
    userInput = input("What word would you like to hash? ")
    print("Hashed Value: \n",sha256(userInput.encode('utf-8')).hexdigest())
  elif userInput == "createacc" and location["rank"] == "owner":
    while True:
      usernamer = input("Please type in the new username: ")
      if len(usernamer) > 3 and usernamer.lower() != "username" and usernamer[0] != "=" and usernamer[0] != '+':
        if not any(d['username'] == usernamer for d in records_data):
          print(f"Username valid.")
          break
        else:
          print("Username already taken, please try again.")
      else:
        print("Username has to be more than 3 characters long" if len(usernamer) < 3 else "This is an invalid username, please choose something else")
    while True:
      passwordr = input("Please set the new password: ")
      if len(passwordr) > 3 and passwordr.lower() != "password":
        print("Password valid. Creating new account...")
        break
      else:
        print("The password must be longer than 3 characters..." if len(passwordr) < 3 else "You cannot set the password to 'password'")
    sheet_hash.add_rows(1)
    sheet_hash.update_row(sheet_hash.rows, [[usernamer,sha256(passwordr.encode('utf-8')).hexdigest()]])
    salt = ''.join(random.choice(string.ascii_letters+string.digits+string.punctuation) for i in range(16))
    while checkDuplicate(salt, 7) == True and salt[0] != "=" and salt[0] != "+":
      salt = ''.join(random.choice(string.ascii_letters+string.digits+string.punctuation) for i in range(16))
    sheet_instance.add_rows(1)
    sheet_instance.update_row(sheet_instance.rows, [[usernamer,500,0,"user",salt]])
  
  else:
    print("That's not a command... Please type 'help' for a list of commands.")

print("Exiting Console...")
