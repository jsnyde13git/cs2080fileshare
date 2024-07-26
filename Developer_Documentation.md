# Developer Instructions

## Installation
Below is the step-by-step process used to set up and install the project. For more details and our license please refer to the documents listed on [README](https://github.com/jsnyde13git/cs2080fileshare).

Provided that the user has an AWS account set up already, the user should go to Modules > Launch AWS Academy Learner Lab > Click on “Start Lab”. Once the Color Icon next to the AWS hyperlink turns green, click on the hyperlink. The user should then navigate to “EC2”. If it is not visible on the Console Home page, select “View all Services” and select “EC2”.

Once at the EC2 Dashboard the user will select “Launch instance”, select a server name, ensure that they select the Ubuntu OS, select or create a key pair (login) which will download the .pem file for SSH into the Linux Shell. Under the Network settings, ensure that "Allow SSH traffic from", "Allow HTTPS traffic from the internet" and "Allow HTTP traffic from the internet" are selected  before clicking "launch the instance". 

On the left-hand side of the page, under the Network & Security tab, select “Elastic IPs”. Click “Allocate Elastic IP address. Use the default setting and click “Allocate”. Select the newly allocated IP address on the following pack and select the “Actions” dropdown button, click “Associate Elastic IP address, select your instance name and select “Associate”. The IP address will now be static utilizing the AWS instance.

Move back to the command prompt and continue installation of the LAMP stack.


From here the user can open the command prompt (Linux or Windows), type `cd Downloads`, and select their server and press the connect button. From there select the SSH client tab and copy the text under “Example” to paste into the cmd prompt: 

For example, mine is as follows:

```
C:\Users\blee10\Downloads>ssh -i "jbkey.pem" ubuntu@ec2-44-196-217-250.compute-1.amazonaws.com
```

Once in the following are commands that were implemented to install the Apache server.

```
$ sudo apt update
$ sudo apt upgrade
$ sudo apt install apache2
$ sudo shutdown –r now # alternatively just do sudo systemctl restart apache2
```

Install MySQL for the server. The `-y` flag will automatically answer yes to prompts, allowing the installation to occur non-interactively from one command.

```
$ sudo apt install mysql-server –y 
$ sudo mysql_secure_installation # secure installation
```

Answer the prompts for the secure installation of MySQL

- Enter password strength = High (user preference)
- Remove anonymous = Yes 
- Disallow Root remotely = Yes 
- Remove test database = Yes 
- Reload privilege table = Yes

Install python3 and pip for Flask installation and ensure they are updated.

```
$ sudo apt install python3 python3-pip -y 
$ sudo apt install libapache2-mod-wsgi-py3 -y 
$ sudo apt update 
```

Install OpenSSL for installation and set-up of a self-signed SSL to enable HTTPS (Secure)

```
$ sudo apt install openssl -y
```

(PLEASE NOTE THAT WHILE SOME OF THESE STEPS WILL PROMPT YOU TO RESTART YOUR APACHE SERVER… DO NOT UNTIL THE END OTHERWISE IT WILL CRASH)

Ensure that pip is installed for flask installation later

```
$ sudo apt-get install python3-pip
```

Create a new directory for the installation and implementation of flask

```
$ sudo mkdir /var/www/html/FlaskApp
```

Move into that directory and copy all the files from the GitHub repository.

```
$ cd /var/www/html/FlaskApp
$ sudo git clone https://github.com/jsnyde13git/cs2080fileshare.git
```

Place `flask_.conf` in `/etc/apache2/sites-available` while in the FlaskApp directory

```
$ sudo mv cs2080fileshare/thing\ to\ put\ in\ etc\ apache\ sites-available/flask_.conf /etc/apache2/sites-available
```

Enabling the flask site (telling Apache to use this)

```
$ sudo a2ensite flask_
```

Disabling the default Apache server (Debian or any other enabled sites; a2dissite on its own will show all sites available)

```
$ sudo a2dissite 000-default
```

Installing the virtual environment in cs2080fileshare directory

```
$ cd /var/www/html/FlaskApp/cs2080fileshare/
$ sudo apt install python3.12-venv
$ sudo python3 -m venv .venv
```

Activating the virtual environment

```
$ source .venv/bin/activate
```

Install flask in the virtual environment

```
$ sudo /var/www/html/FlaskApp/cs2080fileshare/.venv/bin/python -m pip install flask
```

Install flask bootstrap for the virtual environment flask implementation

```
$ sudo /var/www/html/FlaskApp/cs2080fileshare/.venv/bin/python -m pip install bootstrap-flask
```

Install flask-wtf for text input and file upload

```
$ sudo /var/www/html/FlaskApp/cs2080fileshare/.venv/bin/python -m pip install flask-wtf
```

Go into `flaskapp.wsgi` and where it says `sys.path.insert.blablabla`, check the version of Python in `.venv/lib/python<smth>` and replace the Python version listed with your installed version

```
$ cd /var/www/html/FlaskApp/cs2080fileshare
$ sudo vim flaskapp.wsgi
```

Check that there is a line that says:

```
$ sys.path.insert(0,"/var/www/html/FlaskApp/cs2080fileshare/.venv/lib/python3.12/site-packages")
```

Ensure you are in the virtual environment, go to the directory that has python, and verify it matches that insertion path.

```
$ source .venv/bin/activate
$ cd .venv/lib
$ ls
```

After listing all the files, it should show a directory called `python` with a version name; for example, python3.12, or python3.6. (IF THEY DO NOT MATCH) Go into the `flaskapp.wsgi` file and change the version name in the `sys.path.insert` line to match the name of the directory shown here.

Create the logins.txt file

```
$ cd /var/www/html/FlaskApp/cs2080fileshare
$ sudo touch logins.txt
```

Make a directory called data that all the user files will be stored in and give permissions

```
$ sudo mkdir data
$ cd /var/www/html/FlaskApp
$ sudo chmod -R 777 cs2080fileshare/
```

Install OpenSSL if it isn't already 

Make the directory `ssl` in into /etc/apache2

```
$ sudo mkdir /etc/apache2/ssl
```

Create a self-signed certificate and key for SSL and fill out the questions

```
$ openssl req -x509 -newkey rsa:4096 -nodes -out apache-selfsigned.crt -keyout apache-selfsigned.key -days 365
```

Answers will vary:

- Country Name (2 letter code) [AU]:US
- State or Province Name (full name) [Some-State]: Colorado
- Locality Name (eg, city) []: Colorado Springs
- Organization Name (eg, company) [Internet Widgits Pty Ltd]: UCCS cs2080
- Organizational Unit Name (eg, section) []: Brenden Lee & Jaedon Snyder
- Common Name (e.g. server FQDN or YOUR name) []:localhost
- Email Address []: Provide email address if desired

Move the self-signed certificate and key into `/etc/apache2/ssl`

```
$ sudo mv apache-selfsigned.crt /etc/apache2/ssl
$ sudo mv apache-selfsigned.key /etc/apache2/ssl
```

Enabling the module that will allow for https redirect

```
$ sudo a2enmod rewrite
$ sudo a2enmod ssl
```

Restart the Apache server as the final step

```
$ sudo systemctl restart apache2
```

## Using the Webpage

To reach the established website you will need to go to the AWS instances page again and if you click on the server, information will populate below. Both the “Public IPv4 address” and the “Public IPv4 DNS” will have hyperlinks that say “open address” which will take you directly to the website. Since it is a self-signed certificate, it will give a warning that says that the website is not secure. This is normal for this type of certificate.

To start up the server:

```
$ sudo apachectl start
```

To shut down the server:

```
$ sudo apachectl stop
```

To reload the server after making code changes:

```
$ sudo systemctl reload apache2
$ sudo systemctl restart apache2
```

These commands can be run from any directory. 

To create an account, visit the webpage and click Register Account under the login menu, or go to `<sitename>/register`.

To log in, visit the webpage and log in. 

Both logging in and registering an account will redirect you to the file management page. You may also visit this page by visiting `<sitename>/files`.

To upload a file, select a file using the Browse Files button, then hit upload. To replace or update a file, simply upload a file with the same name. 

To download a file, click the appropriate link in the list of uploaded files. 

To share a file with others, have them log into the site. Then, right-click the appropriate link and select Copy Link, then send the link to them. 

By default, only you may download your files. To allow others to download, type each username who you want to allow access to into the "users allowed to download" text box, separated by commas. Then, click submit. For example, to allow `user1` and `testuser` to download your files, type in `user1,testuser`.

[Github Link](https://github.com/jsnyde13git/cs2080fileshare)
