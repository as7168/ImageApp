import os
from flask import Flask, render_template, request, redirect, url_for, flash, Response, send_from_directory
from werkzeug.utils import secure_filename
from flask.ext.mysql import MySQL
from flask_paginate import Pagination
from dbCreds import DATABASE_USER, DATABASE_PASSWORD, DATABASE, DATABASE_HOST

#getting the path for the routes.py file
APP_ROOT = os.path.dirname(os.path.abspath(__file__)) 
#path for the upload folder for uploading images
UPLOAD_FOLDER = os.path.join(APP_ROOT, 'uploads')		
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
PER_PAGE = 10

#creating an instance of MySQL 
mysql = MySQL()

#creating an instance of flask app
app = Flask(__name__)

#configuring the upload folder
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

#this is used to make flash work
app.secret_key = 'random string'

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = DATABASE_USER
app.config['MYSQL_DATABASE_PASSWORD'] = DATABASE_PASSWORD
app.config['MYSQL_DATABASE_DB'] = DATABASE
app.config['MYSQL_DATABASE_HOST'] = DATABASE_HOST
mysql.init_app(app)

#function to connect to the database
def connection():
	conn = mysql.connect()
	c = conn.cursor()
	return c, conn

#function to disconnect from the database
def disconnect(conn):
	conn.close()

#function to check if the uploaded file is allowed by checking its extension
def check_extension(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

#this function takes in all the images and page number and returns the images that are supposed to be on that page number
def get_images_for_page(all_images, page_number):
	new_list = []
	count = len(all_images)
	i = (page_number-1)*10							#if page number = 1, then this value will be 0
	while i <= ((page_number*10)-1) and i < count:	#and this value will be 9; So page one will contain images 0 through 9
		new_list.append(all_images[i])
		i += 1
	return new_list

#home page
@app.route("/", methods=['GET', 'POST'])
def index():	
	if request.method == 'POST':						#if submit button is pressed
		username = request.form['uname']				#get values from the index.html form
		password = request.form['pswd']
		if username == '':								#if username is blank
			flash('Please enter a valid username and password')
		else:											#if username is not blank
			c, conn = connection()						#connect to the database		
			c.execute('''select passwd from users where username=%s''', username)		#get the password from the database
			passwd = c.fetchone()
			if(passwd is not None):						#if the username exist in the database
				if(str(passwd[0]) == password):			#check if the entered password matches the password in the database
					flash('Login Successful')
					return redirect(url_for('user_index', user = username))
				else:
					flash('Incorrect Password!')		
					return redirect(url_for('index'))
			else:
				flash('User not Found!')
				return redirect(url_for('index'))
			disconnect(conn)							#disconnect from the database

	return render_template("index.html")


#Home page for each user
@app.route("/<user>/", methods=['GET', 'POST'])
def user_index(user):
	if request.method == 'POST':					#if upload button is pressed in idex2.html 
		c, conn = connection()
		if 'file' not in request.files:				#if there is no file in the request
			flash('No file part')

		file = request.files['file']				#get the uploaded file and caption
		text = request.form['caption']
		
		if file.filename == '':							#if filename is blank, that means no file has been selected
			flash('No file selected')
		elif file and check_extension(file.filename):	#check if the file is allowed by checking its extension
			c.execute('''select MAX(img_id) from images where usr_name=%s''', user)			#get the maximum img_id for user = user
			maxid = c.fetchone()
			filename = secure_filename(file.filename)
			file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))					#save the file in uploads folder if filename is secure and extension is allowed
			if maxid[0] is None:						#if there are no images in the database insert image in the database with img_id = 0
				c.execute('''insert into images(caption, img_name, img_id, usr_name) values(%s, %s, %s, %s)''', (text, filename, '0', user))
				conn.commit()
			else:										#insert image in the database with img_d = max_id+1
				c.execute('''insert into images(img_id, caption, img_name, usr_name) values(%s, %s, %s, %s)''', (maxid[0]+1, text, filename, user))
				conn.commit()
			redirect(url_for('user_index', user = user))
			flash('Upload Complete')
		else: 						#if the extension is not allowed
			flash('File not allowed')
		disconnect(conn)
	return render_template("index2.html", user = user)

#displaying uploaded images on a page for sepcific user
@app.route('/<user>/images/', defaults={'page':1})
@app.route('/<user>/images/page/<int:page>')
def display_image(page, user):
	c, conn = connection()
	c.execute('''select MAX(img_id) from images where usr_name=%s''', (user))
	maxid = c.fetchone()

	#To check if there are any pictures uploaded for that particular user
	if maxid[0] == None:
		disconnect(conn)
		return render_template('gallery.html', user = user)
	else:
		lis = []
		count = 0
		id = maxid[0]
		while id >= 0 :										#get all the images for the user
			c.execute('''select * from images where img_id=%s and usr_name=%s''', (id, user))
			maxid = c.fetchone()
			lis.append(maxid)
			count += 1
			id = id-1
		images= get_images_for_page(lis, page)				#get images for specified page out of all the images
		pagination = Pagination(page=page, per_page=PER_PAGE, total=count)
		disconnect(conn)
		return render_template('gallery.html', pagination=pagination, images= images, user = user)



#function to get images one at a time from uploads folder
@app.route('/uploads/<filename>', methods=['GET'])
def send_image(filename):
	return send_from_directory('uploads', filename)


#To register new users
@app.route('/register', methods=['GET', 'POST'])
def register():
	if request.method == 'POST':			#If the submit button is pressed in the registeration from
		firstname = request.form['fname']	#get all the fields from the form
		lastname = request.form['lname']
		username = request.form['user']
		password = request.form['paswd']

		c, conn = connection()				#check if the username entered already exists in the database
		c.execute('''select * from users where username=%s''', (username))
		count = c.fetchone()
		if count is not None:				#if the username already exists
			flash('User already exist! Please pick another username!')
		else:								#if the username does not exist, insert the user in the database
			c.execute('''insert into users(first_name, last_name, username, passwd) values(%s, %s, %s, %s)''', (firstname, lastname, username, password))
			conn.commit()
			flash('User Registered')
			return redirect(url_for('index'))
		disconnect(conn)
	return render_template('register.html')

if __name__ == "__main__":
	app.run(debug=True)