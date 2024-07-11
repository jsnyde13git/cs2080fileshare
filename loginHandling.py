import hashlib
import secrets
import os

class loginInfo:
    username = ""
    salt = ""
    passhash = ""
    
    def __init__(self, username, salt, passhash):
        self.username = username
        self.salt = salt
        self.passhash = passhash

#internal func; retrieve login info with a given username
#TODO: make this work with mysql
def getLoginInfo(username):
    File = open(r"/var/www/html/FlaskApp/logins.txt", "r")
    filecontent = File.readlines()
    foundUser = False
    userLine = None
    logInfo = None    

    for line in filecontent:
        accData = line.split()
        if accData[0] == username:
            foundUser = True
            userLine = accData
    
    if foundUser:
        #make login info obj with the username, salt, and pass
        logInfo = loginInfo(accData[0], accData[1], accData[2])

    #passHash = hashPass("testpass","testsalt")
    #return loginInfo("testuser", "testsalt", passHash)
    return logInfo

#check if an account under this name has been created
#TODO: make this work with mysql
def hasAccount(username):
    File = open(r"/var/www/html/FlaskApp/logins.txt", "r")
    filecontent = File.readlines()
    hasAcc = False

    for line in filecontent:
        accData = line.split()
        if accData[0] == username:
            hasAcc = True 

    File.close()
    return hasAcc

#internal func; write login info
#TODO: make this work with mysql
def writeLoginInfo(logInfo):
    if not hasAccount(logInfo.username):
        File_object = open(r"/var/www/html/FlaskApp/logins.txt", "a")
        File_object.write(logInfo.username + " " + logInfo.salt + " " + logInfo.passhash + "\n")  
        File_object.close()

#add account to database
def addAccount(username, password):
    salt = secrets.token_hex()
    hashedPass = hashPass(password, salt)
    logInf = loginInfo(username, salt, hashedPass)
    writeLoginInfo(logInf)

#get hash from password + salt
def hashPass(password, salt):
    hashobj = hashlib.sha256()
    hashobj.update(password.encode())
    hashobj.update(salt.encode())
    return hashobj.hexdigest()

#check if password is correct
def checkPassword(username,password):
    logInfo = getLoginInfo(username)
    if not logInfo is None:
        pwHash = hashPass(password, logInfo.salt)
        if(pwHash == logInfo.passhash):
            return True
        else:
            return False
    else:
        return False
