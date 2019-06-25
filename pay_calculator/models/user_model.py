import hashlib
import re
from datetime import date
import psycopg2
from psycopg2 import extras
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import pdfkit

# DATABASE_URL = os.environ.get('db_url', None)

DATABASE_URL = 'postgres://lrfdzdjpnximyq:3f1ddb578e598f054626ac0754752cb27d27d14e492aaab2a3b71dcdf50d4265@ec2-54-235-77-0.compute-1.amazonaws.com:5432/dvq1qp8vsr5hr'

def register_employee(firstname,email,password,password2):
	
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

	
	cursor.execute("insert into users (firstname,username,password,role,creation_date) values (%s,%s,%s,%s,%s)",(firstname.lower(),email.lower(),sha1_password,role,creation_date))
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

def is_admin(username):
	username = username.lower()
	conn = psycopg2.connect(DATABASE_URL, sslmode='require')
	cursor = conn.cursor()

	cursor.execute("select is_admin from users where username = %s ",(username,))
	
	result = cursor.fetchone()
	print(result)

	return result[0]

def get_email_for_employee(firstname,start_date):
	url = 'http://localhost:6543/payslip?firstname='+firstname+'&start_date='+start_date
	# config = pdfkit.configuration(wkhtmltopd'/Users/nagpal/Downloads/JMD/abc/lib/python3.7/site-packages/wkhtmltopdf')
	pdf = pdfkit.from_url(url, False)

	guard_email = 'isha.negi19@gmail.com'
	email = os.environ.get('from_email', None)
	pwd = os.environ.get('from_password', None)

	s = smtplib.SMTP('smtp.office365.com','587')
	s.starttls()
	s.login(email, pwd)

	msg = MIMEMultipart()
	msg['From'] = email
	msg['To'] = guard_email
	msg['Subject'] = 'Payslip'
	body = MIMEText('Dear '+ firstname.upper() , 'plain')
	msg.attach(body)
	msg.attach(MIMEText(file(pdf).read()))
	s.sendmail(email,guard_email, msg.as_string())
	s.quit()
	return True
