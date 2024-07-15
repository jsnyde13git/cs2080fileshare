#!/bin/usr/python
from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm, CSRFProtect
from flask_wtf.file import FileField
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Length
from flask import send_file, session, request
from werkzeug.utils import secure_filename
from os import walk, path, makedirs

import cs2080fileshare.loginHandling as loginHandler

app = Flask(__name__)

bootstrap = Bootstrap5(app)
csrf = CSRFProtect(app)

if __name__ == "__main__":
    app.run(debug = True, ssl_context=('/etc/apache2/ssl/apache-selfsigned.crt', '/etc/apache2/ssl/apache-selfsigned.key'))

#form for logging in
class LoginForm(FlaskForm):
    username = StringField("username:", validators=[DataRequired(), Length(5, 40)])
    password = PasswordField("password:", validators=[DataRequired(), Length(5,40)])
    submit = SubmitField('Submit')

#form to register an account
class RegisterForm(FlaskForm):
    username = StringField("username:", validators=[DataRequired(), Length(5,40)])
    password = PasswordField("password:", validators=[DataRequired(), Length(5,40)])
    confirmpassword = PasswordField("confirm password:", validators=[DataRequired(), Length(5,40)])
    submit = SubmitField('Submit')

#form to upload a file
class UploadForm(FlaskForm):
    upload_file = FileField()
    submitupl = SubmitField('Upload')

#form to edit user permissions
class PermissionForm(FlaskForm):
    allowedUsers = StringField("users allowed to download:")
    submit = SubmitField("Submit")


#gets a list of all files associated with a given username
def getUserFileList(username):
    filepath = "/var/www/html/FlaskApp/cs2080fileshare/data/" + username
    filenames = next(walk(filepath), (None, None, []))[2]
    return filenames

#formats a list of user files in a set of html links; see user.html for where this would be inserted
def getUserContent(username):
        filelist = getUserFileList(username)
        fileHtmlList = ""
        for filename in filelist:
            fileHtmlList = fileHtmlList + '<br><a href="/download?user='+ username + '&file=' + filename + '">Download ' + filename + '</a>'
        return fileHtmlList

#gets the file path of where a particular file would be stored
def getFilePath(username, filename):
    return "/var/www/html/FlaskApp/cs2080fileshare/data/" + username + "/" + filename


#main login screen
@app.route("/", methods=["GET", "POST"])
def index():
    form = LoginForm()
    uplForm = UploadForm()
    message = "" #this displays under the login form and indicates if the login was successful
    
    # check login
    if form.submit.data and form.validate_on_submit():
        username = form.username.data
        form.username.data = ""
        password = form.password.data
        form.password.data = ""
        loginSuccess = loginHandler.checkPassword(username, password)

        #successful login; add user to session and redirect them to the file management screen
        if loginSuccess:
            message = "Login successful; logged in as " + username
            session["username"] = username
            return redirect("/files", code=302)
        #unsuccessful login; give error
        else:
            message = "Login unsuccessful"

    #display page
    return render_template("index.html", form=form, message=message)


#this is the user page; where the user uploads/downloads files and changes permissions
@app.route("/files", methods=["GET", "POST"])
def files():
    form = UploadForm()
    permissionForm = PermissionForm()

    #check to ensure there's a logged in user, then display content relevant to user
    if "username" in session and session["username"]:
        
        #file upload
        if form.submitupl.data and form.validate_on_submit():
            if form.upload_file.data:

                #create a secure filename and construct the filepath
                filename = secure_filename(form.upload_file.data.filename)
                filepath = "/var/www/html/FlaskApp/cs2080fileshare/data/" + session["username"]

                #if the user doesn't have a folder yet, create the folder before saving
                if not path.exists(filepath):
                    makedirs(filepath)

                #save the file
                form.upload_file.data.save(filepath + "/" + filename)

        #display the user's page, including list of file download links (via getUserContent), the upload form, and the permissions form
        return render_template("user.html", username=session["username"], uploadform = form, permform=permissionForm, usercontent = getUserContent(session["username"]))

    #if user is not logged in, give an error
    else:
        return "<p>ERROR: Not logged in</p>"


#account registration page
@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    message = ""
    
    #process registration
    if form.validate_on_submit():
        username = form.username.data
        form.username.data = ""
        password = form.password.data
        form.password.data = ""
        confpassword = form.confirmpassword.data
        form.confirmpassword.data = ""
        
        #ensure the username isn't taken
        if not loginHandler.hasAccount(username):

            #check that password and "confirm password" fields match
            if password == confpassword:

                #if they match, create an account by adding it to logins.txt via loginHandler and redirect the user to the file management screen
                loginHandler.addAccount(username, password)
                message = "registration successful"
                session["username"] = username
                return redirect("/files", code=302)

            else:
                #if password and password confirmation don't match: 
                message = "password and confirm password don't match"
        else:
            #if trying to register as an already existing user:
            message = "username taken; choose an alternate one"
    
    #display registration page
    return render_template("register.html", form=form, message=message)


#page to download a file; this takes the form <sitename>/download?user=<user>&file=<filename>, with <filename> and <user> requesting the given filename on the given username's account
@app.route("/download", methods=["GET", "POST"])
def download():
    #get username from url arguments
    username = request.args.get("user", None)

    #check if user is logged in or an allowed user
    if username == session["username"]:
        
        #if the user is logged in: get the filename
        filename = request.args.get("file", None)
        #check that file name has been specified, and that it's a valid file on the user's account
        if filename and filename in getUserFileList(username):
            #get the filepath of the file, and send it to the user for download
            filepath = getFilePath(username, filename)
            return send_file(filepath, as_attachment=True)
        else:
            #if filename is blank, display error
            return "<p>ERROR: Invalid filename</p>"
    else:
        #if user is not logged in or allowed, display error
        return "<p>ERROR: No access</p>"
