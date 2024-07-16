This serves as the README file to explain the application, its purpose, and give credit to those who worked on it as well as links that were used. For instructions on the installation please refer to 


Linux based Webserver

This document serves as instructions for the setting up of a Linux based web server for file sharing utilizing an Amazon Web Services instance of Ubuntu, Apache web server, MySQL (MariaDB), Python, and Flask with SSL. 
This application, once set up, will host a python-flask web server that will be SSL secure and allow users to sign in and upload or download files from the server. This is an example of a LAMP (Linux, Apache, MySQL, and Python/PHP/Perl) stack which is the standard of implementing a Linux web server. 
The AWS Ubuntu instance was used because it was the method shown in UCCS’s CS2080 Unix course and made sense to get help with troubleshooting. Apache and MySQL were used based on the stack's complementation of each other. Apache's Debian web server handles the user interface over the Internet, and MySQL handles the database. This project did not dive into MySQL utilization.
The language of choice for the project was Python and thus Flask was used to properly interface with the Apache server. This choice was based on the project team members' familiarity with the language.
Challenges faced in the project were using unfamiliar technology, troubleshooting errors, and time management. There were various web frameworks and content management systems that we investigated and had to decide upon which type to use. Hesitation and excessive caution on the initial set up on the web server cost us time and we ended up not being able to complete all the initial goals for the project. Troubleshooting various errors and server crashes was time consuming due to lack of familiarity, but after enabling debugging commands it eased the process.
Looking towards the future with this project, we hope to complete encryption/decryption handling for files on the server. This would include changing the interaction with users, managing the encryption for additional users, additional files, and location of the encryption keys. While privacy is a must in modern day technology, this was a task that fell through the cracks.

Credits

Project Partners: Brenden Lee and Jaedon Snyder
Helpful Links:
https://www.digitalocean.com/community/tutorials/how-to-install-the-apache-web-server-on-debian-11 (Used other links within the website)
https://www.digitalocean.com/community/tutorials/how-to-set-up-an-apache-mysql-and-python-lamp-server-without-frameworks-on-ubuntu-14-04 
https://www.digitalocean.com/community/tutorials/how-to-make-a-web-application-using-flask-in-python-3 
https://www.geeksforgeeks.org/flask-wtf-explained-how-to-use-it/ 
https://repost.aws/knowledge-center/ec2-linux-ubuntu-install-ssl-cert 
https://blog.miguelgrinberg.com/post/running-your-flask-application-over-https
https://www.reddit.com/r/flask/comments/108cb5x/cannot_import_name_bootstrap5_from_flask_bootstrap/

For our license information, please refer to the LICENSE document.
