# Directories
- client: HTML5/JavaScript Front-end application.
- evaluation: Python modules for invariance tests
	- Oxford: Images of Oxford Buildings Dataset
	- Testbilder: Further images for invariance tests
- server: Flask application modules
	- Templates: Contains Jinja2-Template for buildings overview page
- uploads: Images of buildings used for matching.
- database: Dump of MySQL database.

# Backend
The flask application must be installed on a server along with the following packages:
- Flask
- Flask-Cors
- Flask-SQLAlchemy
- mysqlclient
- numpy                 (Version: 1.14.5)  
- opencv-contrib-python (Version: 3.4.2.17)

You also need to install the MySQL building database on the server. You can find a dump
in the database directory. Please adjust the database connection in flask_app.py
after installing.

# Frontend
While it is possible to run the application by opening the index.html locally,
this will cause some background errors. Since the application is a Progressive Web App,
it should be installed on a server and run from there (using HTTPS only).

Supported browsers are Chrome 80+ and Firefox 74+.

You can install the application on an Android Device. Follow these instructions to do so:
https://support.google.com/chrome/answer/9658361?co=GENIE.Platform%3DAndroid&hl=en

Permissions need to be given for the device camera and location.


# Author Christof Wittmann