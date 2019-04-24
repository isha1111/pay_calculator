from pyramid.view import view_config
from datetime import date
from dateutil import parser
from datetime import datetime 
from datetime import timedelta
from pay_calculator.models import employee_model as Employee
import json
# import psycopg2

@view_config(route_name='employee_add', renderer='../templates/employee/employee_add.mako')
def employee_add(request):
	return {'project':'PAY CALCULATOR'}

@view_config(route_name='save_bulk_employee', renderer='../templates/employee/save_bulk_employee.mako')
def save_bulk_employee(request):
	guard_data = request.POST.get('guard_data')
	Employee.save_bulk_employee(guard_data)
	return {'project':'PAY CALCULATOR'}

@view_config(route_name='employee_save', renderer='../templates/employee/employee_save.mako')
def employee_save(request):
	firstname = request.params.get('firstname')
	lastname = request.params.get('lastname')
	dob = request.params.get('dob')
	gender = request.params.get('gender')
	phone = request.params.get('phone')
	email = request.params.get('email')
	security_license = request.params.get('security_license')
	security_license_expiry = request.params.get('security_license_expiry')
	awards = request.params.get('awards')
	baserate = request.params.get('baserate')
	bsb = request.params.get('bsb')
	account = request.params.get('account')
	notes = request.params.get('notes')

	Employee.add_employee_to_database(firstname,lastname,dob,gender,phone,email,security_license,security_license_expiry,awards,baserate,bsb,account,notes)

	return {'project':'PAY CALCULATOR'}

@view_config(route_name='send_guard_reminder', renderer='../templates/employee/send_guard_reminder.mako')
def send_guard_reminder(request):
	return {'project':'PAY CALCULATOR'}	

@view_config(route_name='send_email_to_guards', renderer='../templates/employee/send_email_to_guards.mako')
def send_email_to_guards(request):
	roaster_data = request.POST.get('roaster_data')
	Employee.send_email_to_guards(roaster_data)
	return {'project':'PAY CALCULATOR'}

@view_config(route_name='search_employee', renderer='../templates/employee/search_employee.mako')
def search_employee(request):
	return {'project':'PAY CALCULATOR'}

@view_config(route_name='fetch_employee', renderer='string')
def fetch_employee(request):
	firstname = request.params.get('firstname')
	lastname = request.params.get('lastname')
	security_license = request.params.get('security_license')
	data = Employee.find_employee(firstname,lastname,security_license)
	print(data)
	return json.dumps(data)