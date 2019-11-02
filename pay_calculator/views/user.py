import json
from pyramid.view import view_config
import pyramid.httpexceptions as exc
from pyramid.httpexceptions import HTTPFound

from pay_calculator.models import user_model as User


@view_config(route_name='login', renderer='../templates/user/login.mako')
def login(request):
	return {'project':'PAY CALCULATOR','username':'','error':''}

@view_config(route_name='logout', renderer='../templates/user/login.mako')
def logout(request):
	ses = request.session
	if 'username' in ses:
		del ses['username']
	if 'pwd_cookie' in ses:
		del ses['pwd_cookie']
	request.session.invalidate()
	request.response.delete_cookie('username')
	request.response.delete_cookie('password')
	raise exc.HTTPFound(request.route_url("login"))
	return {'project':'PAY CALCULATOR','username':''}

@view_config(route_name='forgot_password', renderer='../templates/user/forgot_password.mako')
def forgot_password(request):
	return {'project':'PAY CALCULATOR','username':''}

@view_config(route_name='reset_password', renderer='../templates/user/reset_password.mako')
def reset_password(request):
	password = request.params.get('password')
	password2 = request.params.get('password2')
	email = request.params.get('email')

	confirmation_msg = User.update_employee(email,password,password2)

	return {'project':'PAY CALCULATOR','username':'','confirmation_msg': confirmation_msg}

@view_config(route_name='register', renderer='../templates/user/register.mako')
def register(request):
	firstname = request.params.get('firstname')
	password = request.params.get('password')
	password2 = request.params.get('password2')
	email = request.params.get('email')
	confirmation_msg = ''

	if  ((firstname == '') and (email == '')) or ((firstname is None) and (email is None)):
		return {'project':'PAY CALCULATOR','firstname':firstname,'email':email,'confirmation_msg': confirmation_msg,'username':''}

	confirmation_msg = User.register_employee(firstname,email,password,password2)

	if confirmation_msg =='Successfully created':
		raise exc.HTTPFound(request.route_url("confirm_user_registration"))

	return {'project':'PAY CALCULATOR','firstname':firstname,'email':email,'confirmation_msg': confirmation_msg,'username':''}	

@view_config(route_name='log_user', renderer='../templates/user/login_error.mako')
def log_user(request):
	email =request.params.get('email')
	password = request.params.get('password')
	result = User.find_user(email,password)

	if result is None:
		return {'project':'PAY CALCULATOR','error':'Username or Password is not correct'}
	else:
		pwd_cookie = User.create_cookie_in_md5(email,password)
		request.response.set_cookie('username',email)
		request.response.set_cookie('password',pwd_cookie)
		session = request.session
		session['username'] = email
		session['pwd_cookie'] = pwd_cookie
		response = HTTPFound(location='/', headers=request.response.headers)
		return response

@view_config(route_name='confirm_user_registration', renderer='../templates/user/confirm_user_registration.mako')
def confirm_user_registration(request):
	return {'project':'PAY CALCULATOR','username':''}
