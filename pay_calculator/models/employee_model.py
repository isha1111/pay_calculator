import psycopg2
from psycopg2 import extras
import json
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

DATABASE_URL = 'postgres://lrfdzdjpnximyq:3f1ddb578e598f054626ac0754752cb27d27d14e492aaab2a3b71dcdf50d4265@ec2-54-235-77-0.compute-1.amazonaws.com:5432/dvq1qp8vsr5hr'

def add_employee_to_database(firstname,lastname,dob,gender,phone,email,security_license,security_license_expiry,awards,baserate,bsb,account,notes):

	conn = psycopg2.connect(DATABASE_URL, sslmode='require')
	cursor = conn.cursor()
	cursor.execute("insert into employees (firstname,lastname,date_of_birth,gender,mobile,email,security_license,security_license_expiry,award_type,flat_rate,bsb,account,notes) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(firstname.lower(),lastname.lower(),dob,gender,phone,email,security_license,security_license_expiry,awards,baserate,bsb,account,notes))
	conn.commit()
	cursor.close()
	conn.close()

def delete_employee(emp_id):
	print(type(emp_id))
	conn = psycopg2.connect(DATABASE_URL, sslmode='require')
	cursor = conn.cursor()
	cursor.execute("delete from employees where employee_id = %s ",(emp_id,))
	conn.commit()
	cursor.close()
	conn.close()

def find_employee(firstname,lastname,security_license):
	sql = 'select * from employees'

	where = []
	params= []

	firstname = firstname.lower()
	lastname = lastname.lower()

	if firstname != '':
		where.append("firstname = %s")
		params.append(firstname)
	if lastname != '':
		where.append("lastname = %s")
		params.append(lastname)
	if security_license != '':
		where.append("security_license = %s")
		params.append(security_license)

	params = tuple(params)
	if where:
		sql = '{} WHERE {}'.format(sql, ' AND '.join(where))

	conn = psycopg2.connect(DATABASE_URL, sslmode='require')
	cursor = conn.cursor()
	cursor.execute(sql,params)
	result = cursor.fetchall()
	cursor.close()
	conn.close()

	emp_obj = []
	for row in result:
		temp_obj = {}
		temp_obj["employee_id"] = row[0]
		temp_obj["firstname"] = row[1]
		temp_obj["lastname"] = row[2]
		temp_obj["email"] = row[6]
		temp_obj["phone"] = row[5]
		temp_obj["security_license"] = row[19]
		emp_obj.append(temp_obj)
	return emp_obj

def save_bulk_employee(guard_data):
	conn = psycopg2.connect(DATABASE_URL, sslmode='require')
	cursor = conn.cursor()
	guard_data = json.loads(guard_data)
	list_of_guard_data = guard_data.split('\n')

	values_list = []
	row_num = 1
	for row in list_of_guard_data:
		temp_obj = {} 
		if row != '' and row_num !=1:
			row = row.split('\t')

			names = row[0].split(' ')
			counter = 0
			lname = ''
			for name in names:
				if counter == 0:
					fname = name
					counter = 1
				else:
					if counter == 1:
						lname = lname + name
						counter = 2
					else:
						lname = lname + ' ' + name
			phone = row[1]
			email = row[2]
			security_license = row[3]
			lname = lname.rstrip()
			security_license_expiry = row[4]
			values = (fname.lower(),lname.lower(),phone,email,security_license,security_license_expiry)
			values_list.append(values)
		row_num = row_num + 1

	extras.execute_values(cursor,"insert into employees (firstname,lastname,mobile,email,security_license,security_license_expiry) values %s", values_list)
	conn.commit()
	cursor.close()
	conn.close()


def send_email_to_guards(roaster_data):
	messages = {}
	days = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
	roaster_data = json.loads(roaster_data)

	fname_list = []
	lname_list = []
	for key,value in roaster_data.items():
		list_of_roaster_data = value.split('\n')
		for row in list_of_roaster_data:
			row = row.split('\t')
			temp_obj = {}
			if (len(row) > 7):
				fname = row[3].lower()
				lname = row[4].lower()
				fullname = fname + " " + lname
				start_time = row[2]
				finish_time = row[6]
				hours = row[7]

				if fname == '':
					continue
				else:
					if fullname not in messages and fullname != 'first name surname':
						messages[fullname] = []
						fname_list.append(fname)
						lname_list.append(lname)
					# check if it is date row
					day = row[0]
					if any(word in day for word in days):
						continue
					else:
						messages[fullname].append('Your shift start at '+ start_time + ' and finishes at ' + finish_time  + '.\n') 

	# # now send email
	s = smtplib.SMTP('smtp.office365.com','587')
	s.starttls()
	s.login("sam@rsspersonnel.com.au", "410600@Aa")

	name_to_email = {}
	left_out_email = []
	# check database
	conn = psycopg2.connect(DATABASE_URL, sslmode='require')
	cursor = conn.cursor()
	for fname in fname_list:
		index_val = fname_list.index(fname)
		lname = lname_list[index_val]
		cursor.execute("select firstname,lastname,email from employees where firstname = %s and lastname = %s", (fname.lower(),lname.lower(),))
		result = cursor.fetchone()
		if result is not None:
			name_to_email[fname.lower() + " " + lname.lower()] = result[2]
		else:
			left_out_email.append(fname.lower() + " " + lname.lower())
	cursor.close()
	conn.close()
	for key in messages:
		msg = MIMEMultipart()
		if key in name_to_email:
			guard_email = name_to_email[key]
			msg['From'] = 'sam@rsspersonnel.com.au'
			msg['To'] = guard_email
			msg['Subject'] = 'Shift Roaster'
			shift_text = ''
			for shift in messages[key]:
				shift_text = shift_text + ' ' +shift
			body = MIMEText('Dear '+ key.upper() + '\n' + shift_text, 'plain')
			msg.attach(body)
			s.sendmail("sam@rsspersonnel.com.au",guard_email, msg.as_string())
		else:
			left_out_email.append(key)
		

	# anybody left out
	list(set(left_out_email))
	msg = MIMEMultipart()
	msg['From'] = 'sam@rsspersonnel.com.au'
	msg['To'] = 'sam@rsspersonnel.com.au'
	msg['Subject'] = 'Shift Roaster'
	shift_text = ''
	body = MIMEText('Please email below guard as their email was not found in database' + '\n' + str(left_out_email), 'plain')
	msg.attach(body)
	s.sendmail("sam@rsspersonnel.com.au","sam@rsspersonnel.com.au", msg.as_string())
	return messages