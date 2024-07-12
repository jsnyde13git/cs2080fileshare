#!/usr/bin/python
import sys
import logging
logging.basicConfig(stream=sys.stderr)
project_home = "/var/www/html/FlaskApp"
if project_home not in sys.path:
	sys.path = [project_home] + sys.path
#sys.path.insert(0,"/var/www/html/FlaskApp/")


from cs2080fileshare.__init import app as application
application.secret_key = 'askjfahfbakjdbfkbj'
