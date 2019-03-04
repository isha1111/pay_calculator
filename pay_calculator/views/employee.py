from pyramid.view import view_config
from datetime import date
from dateutil import parser
from datetime import datetime 
from datetime import timedelta
# import psycopg2

DATBASE_URL = 'postgres://lrfdzdjpnximyq:3f1ddb578e598f054626ac0754752cb27d27d14e492aaab2a3b71dcdf50d4265@ec2-54-235-77-0.compute-1.amazonaws.com:5432/dvq1qp8vsr5hr'

@view_config(route_name='employee_add', renderer='../templates/employee/employee_add.mako')
def employee_add(request):
	return {'project':'PAY CALCULATOR'}

@view_config(route_name='employee_save', renderer='../templates/employee/employee_save.mako')
def employee_save(request):
	firstname = request.params.get('firstname')
	lastname = request.params.get('lastname')
	dob = request.params.get('dob')
	gender = request.params.get('gender')
	phone = request.params.get('phone')
	email = request.params.get('email')
	awards = request.params.get('awards')
	baserate = request.params.get('baserate')

	# conn = psycopg2.connect(DATABASE_URL, sslmode='require')
	# cursor = conn.connect()
	# cursor.execute("insert into employees")
	# conn.commit()
	# cursor.close()
	# conn.close()

	return {'project':'PAY CALCULATOR'}