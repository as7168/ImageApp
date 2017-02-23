# ImageApp
Image upload application for Application Security class

>I have named my application 'SNAPOSE'

>The devlopment of Snapose was completed in Windows based environment. Python (Flask) and MySQL DBMS were used to serve the web application.
>In order to run the application, a database needs to be setup using MySQL with two tables named images and users. The configuration and credentials to access the database needs to be stored in the python file _XXXX_
>Tables images and users in the database must have the following columns:

************images**************
img_id|usr_name|caption|img_name

**************users*****************
username|first_name|last_name|passwd

>After setting up the database, you need to make sure you have python, and all the python modules that are used in the application installed in your system to make it work.
>write the name of the modules used

>After you unzip the file, please make sure, the location of folders and files are not changed.
>Go to the App folder and run the following command:
	sudo python routes.py
>This command should start a local server on port 5000 and the application should be up and running.
>You will be able to access the application by typing 'localhost:5000' on your web browser.
>you should be able to register users, login users, logout users, upload images for specific users and view each users uploaded images. You can only see 10 images per page.

