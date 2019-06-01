import json
from pyramid.view import view_config
import pyramid.httpexceptions as exc
from pay_calculator.models import user_model as User


@view_config(route_name='login', renderer='../templates/user/login.mako')
def login(request):
	return {'project':'PAY CALCULATOR'}

@view_config(route_name='register', renderer='../templates/user/register.mako')
def register(request):
	firstname = request.params.get('firstname')
	lastname = request.params.get('lastname')
	password = request.params.get('password')
	password2 = request.params.get('password2')
	email = request.params.get('email')
	confirmation_msg = ''

	if  ((firstname == '') and (lastname == '') and (email == '')) or ((firstname is None) and (lastname is None) and (email is None)):
		return {'project':'PAY CALCULATOR','firstname':firstname,'lastname':lastname,'email':email,'confirmation_msg': confirmation_msg}

	confirmation_msg = User.register_employee(firstname,lastname,email,password,password2)

	if confirmation_msg =='Successfully created':
		raise exc.HTTPFound(request.route_url("confirm_user_registration"))

	return {'project':'PAY CALCULATOR','firstname':firstname,'lastname':lastname,'email':email,'confirmation_msg': confirmation_msg}	

@view_config(route_name='confirm_user_registration', renderer='../templates/user/confirm_user_registration.mako')
def confirm_user_registration(request):
	return {'project':'PAY CALCULATOR'}