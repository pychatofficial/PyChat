import os
import random
import math
import replit
import time
import requests
import turtle
from replit import db
from datetime import date
from num2words import num2words
import firebase_admin
from firebase_admin import credentials
from google.cloud import firestore


cred = credentials.Certificate("pychat-808e6-35b31b8d2664.json")
firebase_admin.initialize_app(cred)


if len(db['currentmessages']) > 10:
  for msg in db['currentmessages']:
    db['msglogs'].append(msg)
  db['currentmessages'].clear()


current_day = date.today()
date_handler = "#" + str(current_day) + "\n"
#print(db['userids'])

def usernamelogin():
  userstemp = []
  replit.clear()
  print("Login")
  userid = int(input("What is your user id? "))
  if userid in db['userids']:
    startup1(userid)
  #for i in db['userids']:
    #userstemp.append(i)
  #if userid in userstemp:
    #startup1(userid)

def loadmessages(userid):
  main(userid)

def guimode(userid):
  screen = turtle.Screen()
  screen.title("PyChat (GUI Mode)")
  while True:
    temp1 = screen.textinput("Message", "At any time, type EXIT in any text input to return to messages. Type Y to continue.")
    if temp1 == "EXIT":
      replit.clear()
      main(userid)
    else:
      break
  replit.clear()
  print("Remember that you can also receive info in the console, here!")
  turtle.write("Main Chat")
  for message in db['currentmessages']:
    turtle.write(message)
  while True:  
    debugkey = os.environ['debugkey']
    send = screen.textinput("MessageSender", "Send a message (type cmd for commands) >>> ")
    if send == debugkey:
      debugmode(userid)
    elif send == "cmd":
      maincommands(userid)
    else:  
      db['currentmessages'].append(str("<User:" + str(userid) + ">: " + send))
      for message in db['currentmessages']:
        turtle.write(message)
    
  
  
## not finished /\ use debug mode to activate**
  
def debugmode(userid):
  if userid == 1:
    replit.clear()
    print("***Debug mode activated***")
    print("Activating GUI mode...")
    guimode(userid)
  else:
    replit.clear()
    print("Error 001: Current user id (" + str(userid) + ") unable to access the requested application. Returning to messages in 3")
    time.sleep(1)
    replit.clear()
    print("Error 001: Current user id (" + str(userid) + ") unable to access the requested application. Returning to messages in 2")
    time.sleep(1)
    replit.clear()
    print("Error 001: Current user id (" + str(userid) + ") unable to access the requested application. Returning to messages in 1")
    time.sleep(1)
    replit.clear()
    main(userid)

def startup1(userid):
  replit.clear()
  loadmessages(userid)

def lookupuser(userid):
  replit.clear()
  print("User Lookup")
  print("BY LOOKING UP A USER, IT WILL BE RECORDED WHO YOU LOOKED UP, ALONG WITH YOUR USERID.")
  usertolookup = input("Input the user id of the user you want to lookup (type EXIT to return to chat): ")
  if usertolookup == "EXIT":
    main(userid)
  else:
    if int(usertolookup) in db['userids']:
      for infopacket in db[usertolookup]:
        if infopacket == "power = True":
          print("User: " + usertolookup)
          print("Power++ User = Yes")
        elif infopacket == "power = False":
          print("User: " + usertolookup)
          print("Power++ User = No")
        elif db[usertolookup] == []:
          print("Error 003: Missing Infopacket(s) for user")
          time.sleep(5)
          lookupuser(userid)
      lookupsummary = "Date of lookup: [" + str(current_day) + "] [User : " + str(userid) + " ] looked up [User : " + str(usertolookup) + " ]"
      db["userlookuplogs"].append(str(lookupsummary))
      exit = input("Type 1 to Exit. Type 2 to lookup another user: ")
      if exit == "1":
        replit.clear()
        main(userid)
      else:
        lookupuser(userid)
    else:
      print("Error 002: User does not exist.")
      time.sleep(5)
      lookupuser(userid)

def maincommands(userid):
  print("Commands (type the number of the command you want to execute it):")
  print("1 : Power++ Commands")
  print("2 : Moderator Commands")
  print("3 : User Lookup")
  print("4 : User Settings")
  print("5 : Logout and go back to login screen")
  cmdtemp1 = input("Number of command: ")
  if cmdtemp1 == "1":
    powercommandschk(userid)
  elif cmdtemp1 == "2":
    modcommandschk(userid)
  elif cmdtemp1 == "3":
    lookupuser(userid)
  elif cmdtemp1 == "4":  
    settings(userid)
  elif cmdtemp1 == "5":  
    replit.clear()
    start()

def powercommandschk(userid):
  replit.clear()
  print("Power++ Commands")
  userfile = __import__(str(num2words(int(userid))))
  if userfile.power == True:
    powercommands(userid)
  else:
    print("It doesn't seem like you're a Power++ Member. Exiting... ")
    main(userid)

##def powercommands(userid):

def modcommandschk(userid):
  replit.clear()
  modchk2 = input("Please enter the global moderator PIN code: \n")
  modpin = os.environ['modpin']
  if modchk2 == modpin:
    replit.clear()
    print("PIN correct! Redirecting to moderator commands...")
    time.sleep(5)
    modcommands(userid)
  else:
    replit.clear()
    print("Incorrect PIN.")
    main(userid)
      
def modcommands(userid):
  replit.clear()
  print("Moderator Commands")
  print("1 : Moderate The Chat")
  print("2 : Activate Power++ for a user")
  print("3 : Ban a user")
  print("4 : Unban a user")
  modtemp1 = input("Number of command to execute: ")
  if modtemp1 == "1":
    moderate(userid)
  elif modtemp1 == "2":
    poweractivation(userid)
  elif modtemp1 == "3":
    banuser(userid)
  elif modtemp1 == "4":
    unbanuser(userid)
  
def moderate(userid):
  replit.clear()
  print("Moderation")
  print("\/ Current Messages \/")
  counter = 1
  for message in db["currentmessages"]:
    print("[msg number:" + str(counter) + "] [msg content:" + str(message) + "]")
    counter = counter + 1
  while True:
    modtemp2 = input("Input the number of the message to delete (type EXIT to return to main, type CLEAR to clear all messages): ")
    counter = 1
    if modtemp2 == "EXIT":
      replit.clear()
      main(userid)
    elif modtemp2 == "CLEAR":
      for msg in db['currentmessages']:
        db['msglogs'].append(msg)
      db["currentmessages"].clear()
      db["currentmessages"].append("*/* System (Used as moderator " + str(userid) + ") */* :: Cleared and logged messages.")
      print("Cleared all messages successfully. (The messages were moved to msglogs, and it will be shown that you have cleared the messages.)")
      time.sleep(3)
      moderate(userid)
    else:
      for message in db["currentmessages"]:
        if counter == int(modtemp2):
          db["currentmessages"].remove(message)
          replit.clear()
          print("Moderation")
          print("\/ Current Messages \/")
          counter = 1
          for message in db["currentmessages"]:
            print("[msg number:" + str(counter) + "] [msg content:" + str(message) + "]")
          time.sleep(2)
          print("Deleted Message Successfully.")
          counter = counter + 1
##fix moderation counter error (still!!) i havent removed this comment, its not fixed.../\
  
def poweractivation(userid):
  replit.clear()
  print("Power++ Activation")
  usertoactivate = input("Input the user to activate Power++ for. ")
  db[usertoactivate].remove("power = False")
  with open(str(usertoactivate) + 'py', 'x') as file:
    file.write(date_handler)
    file.write("\npower = True")
  print("Success.")
  time.sleep(3)
  modcommands(userid)
  
def banuser(userid):
  replit.clear()
  usertoban = input("Input the user id of the user to ban: ")
  with open(str(usertoban) + '.py', "a+") as file:
    file.write(date_handler)
    file.write("Banned by: " + str(userid) + "\n")
    file.write("banned = True\n")
  file.close()
  print("Success.")
  time.sleep(3)
  modcommands(userid)
'''
def unbanuser(userid):
  replit.clear()
  usertounban = input(int("Input the user id of the user to unban: "))
  db['userinfo3'].remove("Banned.")
  db[usertounban].append("[Unbanned by: " + userid + " ] [Unbanned on: " + current_day + " ]")
  print("Successfully Unbanned User.")
  time.sleep(3)
  modcommands(userid)
'''
def sendmessage(userid):
  debugkey = os.environ['debugkey']
  send = input("Send a message (type cmd for commands, or type R to reload or to receive a bot message) >>> ")
  if send == debugkey:
    debugmode(userid)
  elif send == "cmd":
    maincommands(userid)
  elif send == "servertest":
    scratchapi(userid)
  elif send == "R" or send == "r":
    from bots547 import reloadbots
    reloadbots(userid)
  else:  
    db['currentmessages'].append(str("<User:" + str(userid) + ">: " + send))
    reloadmessages(userid)

def __init__():
  import os
  from http.server import HTTPServer, CGIHTTPRequestHandler
  # Make sure the server is created at current directory
  os.chdir('.')
  # Create server object listening the port 80
  server_object = HTTPServer(server_address=('', 80), RequestHandlerClass=CGIHTTPRequestHandler)
  # Start the web server
  server_object.serve_forever()

def reloadmessages(userid):
  replit.clear()
  for message in db['currentmessages']:
    print(message)
  sendmessage(userid)
  
def accountcreate():
  replit.clear()
  while True:  
    username = input("Choose a unique username: ")
    if username in db['usernames']:
      newuserid = len(db['userids']) + 1
      print("Your user id is: " + str(newuserid) + ".")
      print("Configuring account...")
      #add a way to check if the user id has infopackets already before adding new ones
      userfile = str(num2words(int(newuserid))) + ".py"
      with open(userfile, "a+") as file:
        file.write("##user created on: " + str(current_day) + "\n")
        file.write(date_handler)
        file.write("power = False\n")
        file.write(date_handler)
        file.write("banned = False\n")
        file.write(date_handler)
        file.write("username = " + username)
      db['userids'].append(newuserid)
      print("Done Configuring!")
      time.sleep(4)
      main(newuserid)
    else:
      print("Already Taken. Retry in 3 seconds.")
      time.sleep(3)
      accountcreate()

def start():
  username = os.environ['REPL_OWNER']
  debugkey = os.environ['debugkey']
  if username in db['bannedusernames']:
    print("Error 100: You have been permanently banned from PyChat.")
  else:
    print("PyChat")
    a = input("Do you have an account? Y/N ")
    if a == "Y":
      usernamelogin()
    elif a == debugkey:
      debugmode(1)
    else:
      accountcreate()

def main(userid):
  ###FIX THIS SO THAT IT DOESNT LET SOMEONE IN ONLY IF THEY'VE BEEN BANNED \/
  ###update: fixed! :)
  replit.clear()
  userfilename = str(num2words(userid))
  userfile = __import__(userfilename)
  if userfile.banned == True:
    while True:
      print("You were banned.")
      print("When unbanned, ask a moderator to check who banned you, and ask them why you were banned.")
      print("(This reloads every ten seconds...)")
      time.sleep(10)
      main(userid)
  replit.clear()
  print("Main Channel")
  for message in db['currentmessages']:
    print(message)
  sendmessage(userid)

def settings(userid):
  replit.clear()
  print("User settings")
  print("1: Change Username")
  print("2: Privacy Settings")
  print("3: Security Settings")
  print("4: PyChat for Windows Setup")
  print("5: Cancel And Return To Chat")
  tempidkwhatnumberitislol = input(str("Input the number of the setting to go to:"))
  if tempidkwhatnumberitislol == "1":
    changeusername(userid)
  elif tempidkwhatnumberitislol == "2":
    privacysettings(userid)
  elif tempidkwhatnumberitislol == "3":
    securitysettings(userid)
  elif tempidkwhatnumberitislol == "4":  
    pychatforwindows(userid)
  elif tempidkwhatnumberitislol == "5":  
    replit.clear()
    main(userid)

def changeusername(userid):
  replit.clear()
  print("Username Changer")
  userfile = __import__(str(num2words(int(userid))))
  print("Your current username is: " + userfile.username)
  print("If you change your username, anyone else could take it.")
  print("If you want to change your username back, you can, as long as someone else didn't claim it already.")
  print("In the New Username Prompt, type CANCEL to cancel the username change.")
  newusername = input("Input your new username (or type CANCEL to cancel.):")
  if newusername == "CANCEL":
    print("Returning to main chat")
    time.sleep(3)
    main(userid)
  elif newusername in db['usernames']:
    print("Username is taken.")
    print("Try again in 3 seconds")
    time.sleep(3)
  else: 
    with open(str(num2words(userid)) + ".py", "a+") as file:
      file.write(date_handler)
      file.write("username = " + "\"" + newusername + "\"")
    print("Changed username successfully!")
    time.sleep(3)
    main(userid)

def scratchapi(userid):
  import websiteunblocker
  '''response = requests.get(str("http://explodingstar.pythonanywhere.com/scratch/api/?endpoint=/studios/33531409/comments"))
  if response.status_code == 200:
    data = response.json()
    print(data)
    import json

# Open the JSON file for reading
    with open('tempjson.json', 'a+') as file:
    # Parse JSON data
      file.write(str(data))
      data = json.load(file)
      os.remove("tempjson.json")

# Display the data
    print(data)
    commentcontent = str(data.content)
    commentauthor = str(data.author.username)
    if commentauthor == "Nicky547" or commentauthor == "nicky547":
      commentauthor = "Nicky: Verified Creator of PyChat"
    import botfunctions as sender
    sender.sendcustom1(commentauthor, commentcontent)
    '''
    
#def privacysettings(userid):
  
#def securitysettings(userid):



#firebase = pyrebase.initialize_app(firebaseConfig)
#db3 = firebase.database()
#storage=firebase.storage()

def pychatforwindows(userid):
  print("Transferring user data...")
  userfiledata = __import__(str(num2words(int(userid))))
  #db = firestore.Client()
  #collection = db.collection('pychatusers')
  #storage.child(str(num2words(int(userid))) + "user").put(str(num2words(int(userid))) + "user")
  #url = storage.child(str(num2words(int(userid))) + "user").get_url(None)
  #authcode = os.environ['authcode']
  firestore_client = firestore.Client.from_service_account_json('pychat-808e6-35b31b8d2664.json')
  windowspassword = str(random.randint(1000, 9999))
  ref = firestore_client.collection('pychatusers')
  doc_ref = ref.document("user" + str(num2words(int(userid))))
  doc_ref.set({
    "userid" : str(userid), "banned" : userfiledata.banned, "testuser" : userfiledata.testuser, "windowspassword" : windowspassword
})
  
  #res = collection.document("user" + str(num2words(int(userid)))).set({
    #"userid" : str(userid), "banned" : userfiledata.banned, "testuser" : userfiledata.testuser
  #})
  #print(res)
  #data = {"userid" : str(userid), "banned" : userfiledata.banned, "testuser" : userfiledata.testuser}

  #db.child("users").push(data)
  print("Finished! Procceed to the windows client to continue.")
  print("Your windows password is " + windowspassword)
  
  

start()