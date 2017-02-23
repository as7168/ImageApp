import os
from flask import Flask, render_template, request, redirect, url_for, flash, Response, send_from_directory
from werkzeug.utils import secure_filename
from flask.ext.mysql import MySQL
from flask_paginate import Pagination

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
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'postgres'
app.config['MYSQL_DATABASE_DB'] = 'snapose'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

#function to connect to the database
def connection():
	conn = mysql.connect()
	c = conn.cursor()
	return c, conn

#function to check if the uploaded file is allowed by checking its extension
def check_extension(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_images_for_page(all_images, page_number):
	new_list = []
	count = len(all_images)
	i = (page_number-1)*10
	while i <= ((page_number*10)-1) and i < count:
		new_list.append(all_images[i])
		i += 1
	return new_list

#displaying uploaded images on a page
@app.route('/<user>/images/', defaults={'page':1})
@app.route('/<user>/images/page/<int:page>')
def display_image(page, user):
	c, conn = connection()
	c.execute('''select MAX(img_id) from images where usr_name=%s''', (user))
	maxid = c.fetchone()
	print('------------------------------------------>')
	#print maxid
	#To check if there are any pictures uploaded
	if maxid[0] == None:
		return render_template('gallery.html', user = user)
	else:
		lis = []
		count = 0
		id = maxid[0]
		#lis.append(maxid)
		while id >= 0 :
			c.execute('''select * from images where img_id=%s and usr_name=%s''', (id, user))
			maxid = c.fetchone()
			#print maxid
			lis.append(maxid)
			count += 1
			id = id-1
		images= get_images_for_page(lis, page)
		#print lis
		pagination = Pagination(page=page, per_page=PER_PAGE, total=count)
		return render_template('gallery.html', pagination=pagination, images= images, user = user)

#function to get images one at a time
@app.route('/uploads/<filename>', methods=['GET'])
def send_image(filename):
	return send_from_directory('uploads', filename)

#home page
#@app.route('/index', methods=['GET', 'POST'])
@app.route("/", methods=['GET', 'POST'])
def index():	
	if request.method == 'POST':
		username = request.form['uname']
		#print('--------------------------------->')
		password = request.form['pswd']
		if username == '':
			flash('Please enter a valid username and password')
		else:
			c, conn = connection()
			c.execute('''select passwd from users where username=%s''', username)
			passwd = c.fetchone()
			print('---------------------------------->')
			print(passwd)
			if(passwd is not None):
				if(str(passwd[0]) == password):
					flash('Login Successful')
					return redirect(url_for('user_index', user = username))
				else:
					flash('Incorrect Password!')
					return redirect(url_for('index'))
			else:
				flash('Incorrect Password!')
				return redirect(url_for('index'))

	return render_template("index.html")

@app.route("/<user>/", methods=['GET', 'POST'])
def user_index(user):
	if request.method == 'POST':
		#flash('hello')
		c, conn = connection()
		if 'file' not in request.files:
			flash('No file part')
		file = request.files['file']
		text = request.form['caption']
		#print('-------------------------------------------->')
		#print(text)
		if file.filename == '':
			flash('No file selected')
		elif file and check_extension(file.filename):
			c.execute('''select MAX(img_id) from images where usr_name=%s''', user)
			maxid = c.fetchone()
			filename = secure_filename(file.filename)
			file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
			if maxid[0] is None:
				c.execute('''insert into images(caption, img_name, img_id, usr_name) values(%s, %s, %s, %s)''', (text, filename, '0', user))
				conn.commit()
			else:
				c.execute('''insert into images(img_id, caption, img_name, usr_name) values(%s, %s, %s, %s)''', (maxid[0]+1, text, filename, user))
				conn.commit()
			redirect(url_for('user_index', user = user))
			flash('Upload Complete')
		else: 
			flash('File not allowed')
	return render_template("index2.html", user = user)

@app.route('/register', methods=['GET', 'POST'])
def register():
	if request.method == 'POST':
		firstname = request.form['fname']
		lastname = request.form['lname']
		username = request.form['user']
		password = request.form['paswd']

		c, conn = connection()
		c.execute('''select * from users where username=%s''', (username))
		count = c.fetchone()
		if count is not None:
			flash('User already exist! Please pick another username!')
		else:
			c.execute('''insert into users(first_name, last_name, username, passwd) values(%s, %s, %s, %s)''', (firstname, lastname, username, password))
			conn.commit()
			flash('User Registered')
			return redirect(url_for('index'))
	return render_template('register.html')

if __name__ == "__main__":
	app.run(debug=True)