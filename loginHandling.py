import hashlib
import secrets
import os

#class to hold a full set of login info; username, password hash, salt, and allowed users
class loginInfo:
    username = ""
    salt = ""
    passhash = ""
    allowedusers = ""

    #constructor; sets the values for user, salt, and password hash
    def __init__(self, username, salt, passhash):
        self.username = username
        self.salt = salt
        self.passhash = passhash
        self.allowedusers = ""

loginFile = r"/var/www/html/FlaskApp/cs2080fileshare/logins.txt"

def getAllowedUsersAsString(username):
    logInfo = getLoginInfo(username)
    if not logInfo is None:
        return logInfo.allowedusers
    else:
        return ""

def getAllowedUsersAsList(username):
    logInfo = getLoginInfo(username)
    if not logInfo is None:
        return logInfo.allowedusers.split(",")
    else:
        return []
#update a user's allowed users
def writeAllowedUsers(username, userList):
    with open(loginFile, "r") as f:
        contents = f.readlines()

    #find the index of the desired user in the file and update the list with the new information
    userIndex = -1
    for index, line in enumerate(contents):
        accData = line.split()
        if accData[0] == username:
            if len(accData) > 3:
                accData[3] = userList
            else:
                accData.append(userList)
            contents[index] = " ".join(accData) + "\n"

    #write the new information to the file
    with open(loginFile, "w") as f:
        f.writelines(contents)

def isUserAllowed(ownerUser, checkedUser):
    #get a list of users
    allowedUsers = getAllowedUsersAsList(ownerUser)
    #return whether the user to check is in allowed user list
    if checkedUser in allowedUsers:
        return True
    else:
        return False

#retrieve login info with a given username; not intended for use outside this file
def getLoginInfo(username):
    #open login file for reading and prepare for search
    File = open(r"/var/www/html/FlaskApp/cs2080fileshare/logins.txt", "r")
    filecontent = File.readlines()
    File.close()
    foundUser = False
    userData = None
    logInfo = None    

    #do a linear search through login file
    for line in filecontent:
        #split account data into a list
        accData = line.split()
        if accData[0] == username:
            foundUser = True
            userData = accData
    
    #if user was found, return a loginInfo object with the user info
    if foundUser:
        #make login info obj with the username, salt, and password hash, in that order
        logInfo = loginInfo(userData[0], userData[1], userData[2])
        #if user has a list of allowed users: add it to the object
        if len(userData) > 3:
            logInfo.allowedusers = userData[3]

    return logInfo

#check if an account under this name has been created; returns boolean
def hasAccount(username):
    File = open(r"/var/www/html/FlaskApp/cs2080fileshare/logins.txt", "r")
    filecontent = File.readlines()
    hasAcc = False #set to true if an account with the given username exists

    #linear search through the file
    for line in filecontent:
        accData = line.split()
        if accData[0] == username:
            hasAcc = True 

    File.close()
    return hasAcc

#append login info to the end of the login file
def writeLoginInfo(logInfo):
    #check to ensure the user doesn't have an existing account; having duplicate accounts would break things
    if not hasAccount(logInfo.username):
        #append user account info to the end of the logins.txt file
        File_object = open(r"/var/www/html/FlaskApp/cs2080fileshare/logins.txt", "a")
        File_object.write(logInfo.username + " " + logInfo.salt + " " + logInfo.passhash + "\n")  
        File_object.close()

#add account to database
def addAccount(username, password):
    #generate a random salt
    salt = secrets.token_hex()
    #create the password hash using the password and salt
    hashedPass = hashPass(password, salt)
    #create login info object using user, salt, and password hash
    logInf = loginInfo(username, salt, hashedPass)
    #append login into to logins.txt
    writeLoginInfo(logInf)

#get hash from password + salt
def hashPass(password, salt):
    #use hashlib to generate a hash
    hashobj = hashlib.sha256()
    #calling update twice is equivalent to calling update once with password and salt concatenated
    hashobj.update(password.encode())
    hashobj.update(salt.encode())
    #hexdigest creates the hash from the passed data
    return hashobj.hexdigest()

#check if password is correct for a given username
def checkPassword(username,password):
    logInfo = getLoginInfo(username)
    #ensure that the user has an account by checking that the login info is non-null
    if not logInfo is None:
        #hash the password, and check that the password hash matches
        pwHash = hashPass(password, logInfo.salt)
        if(pwHash == logInfo.passhash):
            return True
        else:
            return False

    else:
        #if the user doesn't have an account, report login as unsuccessful
        return False
