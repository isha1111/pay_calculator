import hashlib
import re
from datetime import date
import psycopg2
from psycopg2 import extras
import os

DATABASE_URL = os.environ.get('db_url', None)

def register_employee(firstname,lastname,email,password,password2):
	
	role = 'normal'
	creation_date = date.today().strftime('%d-%m-%Y')

	# check password criteria
	rgx = re.compile(r'\d.*?[A-Z].*?[a-z]')
	if rgx.match(''.join(sorted(password))) and len(password) >= 6:
		pwd = password
	else:
		return "Please ensure you have Uppercase letter, lowercase letter and digits in password and minimum 6 characters"

	# check password are same
	if password != password2:
		return "Passwords don't match"

	# check email
	result = re.search('^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$',email)
	if result is None:
		return "This email is not valid, it must be a valid email address"

	# check if user exists in DB
	conn = psycopg2.connect(DATABASE_URL, sslmode='require')
	cursor = conn.cursor()
	cursor.execute("select count(*) from users where username = %s",(email.lower(),))
	result = cursor.fetchall()
	if result[0][0] != 0:
		return "User Exist Already"
	# if not create user
	m = hashlib.sha1()
	m.update(password.encode('utf-8'))
	sha1_password = m.hexdigest()

	
	cursor.execute("insert into users (firstname,lastname,username,password,role,creation_date) values (%s,%s,%s,%s,%s,%s)",(firstname.lower(),lastname.lower(),email.lower(),sha1_password,role,creation_date))
	conn.commit()
	cursor.close()
	conn.close()
	return "Successfully created"

 
def create_cookie_in_md5(username,password): #CRITICAL-2
	username = username.lower()
	m = hashlib.sha1()
	m.update(password.encode('utf-8'))
	sha1_password = m.hexdigest()

	h = hashlib.sha1()
	h.update(username.encode('utf-8') + sha1_password.encode('utf-8'))
	user_and_pwd_md5 = h.hexdigest()

	return user_and_pwd_md5

def find_user(email,password):
	username = email.lower()
	
	m = hashlib.sha1()
	m.update(password.encode('utf-8'))
	sha1_password = m.hexdigest()
	
	conn = psycopg2.connect(DATABASE_URL, sslmode='require')
	cursor = conn.cursor()

	cursor.execute("select count(*) from users where username = %s and password= %s",(username,sha1_password))
	
	result = cursor.fetchall()

	if result[0][0] == 1:
		return "User Found"
	else:
		return None

