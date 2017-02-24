# ImageApp
Image upload application for Application Security class

>I have named my application 'SNAPOSE'

>The devlopment of Snapose was completed in Windows based environment. Python (Flask) and MySQL DBMS were used to serve the web application.
>In order to run the application, a database needs to be setup using MySQL with two tables named images and users. The configuration and credentials to access the database needs to be stored in the python file dbCreds.py.
	
>Tables images and users in the database must have the following columns:
 CREATE TABLE `users` (
  `first_name` varchar(50) NOT NULL DEFAULT '',
  `last_name` varchar(50) NOT NULL DEFAULT '',
  `passwd` char(64) NOT NULL,
  `username` varchar(100) NOT NULL,
  PRIMARY KEY (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8

CREATE TABLE `images` (
  `img_id` int(11) NOT NULL,
  `caption` varchar(255) NOT NULL DEFAULT '',
  `img_name` varchar(100) NOT NULL,
  `usr_name` varchar(100) NOT NULL,
  PRIMARY KEY (`img_id`,`usr_name`),
  KEY `usr_name` (`usr_name`),
  CONSTRAINT `images_ibfk_1` FOREIGN KEY (`usr_name`) REFERENCES `users` (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8


************images**************
img_id|caption|img_name|usr_name

**************users*****************
first_name|last_name|passwd|username 

>After setting up the database, you need to make sure you have python, and all the python modules that are used in the application installed in your system to make it work.
>flask, werkzeug.utils, flask.ext.mysql, flask_paginate

>After you unzip the file, please make sure, the location of folders and files are not changed and there is an 'uploads' folder in the home directory of the application (the directory where routes.py is located)
>Go to the App folder and run the following command:
	sudo python routes.py
>This command should start a local server on port 5000 and the application should be up and running.
>You will be able to access the application by typing 'localhost:5000' on your web browser.
>you should be able to register users, login users, logout users, upload images for specific users and view each users uploaded images. You can only see 10 images per page.

Note: the venv folder in the App folder is the virtual environment that I created for the application.
Note: this application has a lot of security issues, which I did not get enough time to address. I wanted to implement all the functionality manually so that I could understand how things work in flask. I will try to address all the secrity issues in next assignment. 

