import hashlib
import re
from datetime import date
import psycopg2
from psycopg2 import extras

DATABASE_URL = 'postgres://lrfdzdjpnximyq:3f1ddb578e598f054626ac0754752cb27d27d14e492aaab2a3b71dcdf50d4265@ec2-54-235-77-0.compute-1.amazonaws.com:5432/dvq1qp8vsr5hr'


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