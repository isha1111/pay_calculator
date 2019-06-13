from pyramid.view import view_config
from datetime import date
from dateutil import parser
from datetime import datetime 
from datetime import timedelta
import pyramid.httpexceptions as exc
from pay_calculator.models import employee_model as Employee
from pay_calculator.models import auth_model as Auth
import json
# import psycopg2

@view_config(route_name='employee_add', renderer='../templates/employee/employee_add.mako')
def employee_add(request):
	auth_check_pass = Auth.check_user_session(request.session)
	if not auth_check_pass:
		raise exc.HTTPFound(request.route_url("login"))
	return {'project':'PAY CALCULATOR','username':request.session['username']}

@view_config(route_name='save_bulk_employee', renderer='../templates/employee/save_bulk_employee.mako')
def save_bulk_employee(request):
	auth_check_pass = Auth.check_user_session(request.session)
	if not auth_check_pass:
		raise exc.HTTPFound(request.route_url("login"))
	guard_data = request.POST.get('guard_data')
	Employee.save_bulk_employee(guard_data)
	return {'project':'PAY CALCULATOR','username':request.session['username']}

@view_config(route_name='employee_save', renderer='../templates/employee/employee_save.mako')
def employee_save(request):
	auth_check_pass = Auth.check_user_session(request.session)
	if not auth_check_pass:
		raise exc.HTTPFound(request.route_url("login"))
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
	try:
		Employee.add_employee_to_database(firstname,lastname,dob,gender,phone,email,security_license,security_license_expiry,awards,baserate,bsb,account,notes)
		result = 'Successfully saved'
	except:
		result = 'Something went wrong'

	return {'project':'PAY CALCULATOR','result':result,'username':request.session['username']}

@view_config(route_name='save_updated_employee', renderer='string')
def save_updated_employee(request):
	auth_check_pass = Auth.check_user_session(request.session)
	if not auth_check_pass:
		raise exc.HTTPFound(request.route_url("login"))
	emp_id = request.params.get('emp_id')
	print(emp_id)
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
	result = Employee.save_updated_employee(emp_id,firstname,lastname,dob,gender,phone,email,security_license,security_license_expiry,awards,baserate,bsb,account,notes)
	return result

@view_config(route_name='send_guard_reminder', renderer='../templates/employee/send_guard_reminder.mako')
def send_guard_reminder(request):
	auth_check_pass = Auth.check_user_session(request.session)
	if not auth_check_pass:
		raise exc.HTTPFound(request.route_url("login"))
	return {'project':'PAY CALCULATOR','username':request.session['username']}	

@view_config(route_name='send_email_to_guards', renderer='../templates/employee/send_email_to_guards.mako')
def send_email_to_guards(request):
	auth_check_pass = Auth.check_user_session(request.session)
	if not auth_check_pass:
		raise exc.HTTPFound(request.route_url("login"))
	roaster_data = request.POST.get('roaster_data')
	Employee.send_email_to_guards(roaster_data)
	return {'project':'PAY CALCULATOR','username':request.session['username']}

@view_config(route_name='search_employee', renderer='../templates/employee/search_employee.mako')
def search_employee(request):
	auth_check_pass = Auth.check_user_session(request.session)
	if not auth_check_pass:
		raise exc.HTTPFound(request.route_url("login"))
	return {'project':'PAY CALCULATOR','username':request.session['username']}

@view_config(route_name='update_employee', renderer='../templates/employee/update_employee.mako')
def update_employee(request):
	auth_check_pass = Auth.check_user_session(request.session)
	if not auth_check_pass:
		raise exc.HTTPFound(request.route_url("login"))
	return {'project':'PAY CALCULATOR','username':request.session['username']}

@view_config(route_name='view_employee', renderer='../templates/employee/view_employee.mako')
def view_employee(request):
	auth_check_pass = Auth.check_user_session(request.session)
	if not auth_check_pass:
		raise exc.HTTPFound(request.route_url("login"))
	emp_id = request.params.get('emp_id')
	emp_data = Employee.find_employee_by_id(emp_id)
	return {'project':'PAY CALCULATOR','emp_data':emp_data,'username':request.session['username']}

@view_config(route_name='edit_employee', renderer='../templates/employee/edit_employee.mako')
def edit_employee(request):
	auth_check_pass = Auth.check_user_session(request.session)
	if not auth_check_pass:
		raise exc.HTTPFound(request.route_url("login"))
	emp_id = request.params.get('emp_id')
	emp_data = Employee.find_employee_by_id(emp_id)
	return {'project':'PAY CALCULATOR','emp_data':emp_data,'username':request.session['username']}

@view_config(route_name='delete_employee', renderer='../templates/employee/delete_employee.mako')
def delete_employee(request):
	auth_check_pass = Auth.check_user_session(request.session)
	if not auth_check_pass:
		raise exc.HTTPFound(request.route_url("login"))
	return {'project':'PAY CALCULATOR','username':request.session['username']}

@view_config(route_name='delete_employee_from_database', renderer='string')
def delete_employee_from_database(request):
	auth_check_pass = Auth.check_user_session(request.session)
	if not auth_check_pass:
		raise exc.HTTPFound(request.route_url("login"))
	emp_id = request.params.get('id')
	try:
		Employee.delete_employee(emp_id)
		result = "successfully deleted"
	except:
		result = "something went wrong"
	return result

@view_config(route_name='fetch_employee', renderer='string')
def fetch_employee(request):
	auth_check_pass = Auth.check_user_session(request.session)
	if not auth_check_pass:
		raise exc.HTTPFound(request.route_url("login"))
	firstname = request.params.get('firstname')
	lastname = request.params.get('lastname')
	security_license = request.params.get('security_license')
	data = Employee.find_employee(firstname,lastname,security_license)
	return json.dumps(data)