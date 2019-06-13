from pyramid.view import view_config
import pyramid.httpexceptions as exc
from pay_calculator.models import pay_model as Pay
from pay_calculator.models import auth_model as Auth
import json

@view_config(route_name='home', renderer='../templates/index.mako')
def my_view(request):
	auth_check_pass = Auth.check_user_session(request.session)
	if not auth_check_pass:
		raise exc.HTTPFound(request.route_url("login"))
	return {'project': 'PAY CALCULATOR','pay':'','username':request.session['username']}

@view_config(route_name='calculate_payrate', renderer='../templates/pay/pay.mako')
def calculate_payrate(request):
	auth_check_pass = Auth.check_user_session(request.session)
	if not auth_check_pass:
		raise exc.HTTPFound(request.route_url("login"))
	roaster_data = request.POST['roaster_data']
	roaster_data = roaster_data.value
	roaster_data = roaster_data.decode('utf-8')

	state = request.params.get('state')	

	pay_type = request.params.get('pay_type')

	if pay_type == 'jmd_eba':
		pay = Pay.calculate_jmd_eba_rate(roaster_data, state)
		return {'project': 'PAY CALCULATOR','pay':pay,'pay_type':'jmd_eba','username':request.session['username']}

	if pay_type == 'awards':
		pay = Pay.calculate_awards_rate(roaster_data, state)
		return {'project': 'PAY CALCULATOR','pay':pay,'pay_type':'awards','username':request.session['username']}

	if pay_type == 'rss':
		pay = Pay.calculate_rss_rate(roaster_data, state)
		return {'project': 'PAY CALCULATOR','pay':pay,'pay_type':'rss','username':request.session['username']}

@view_config(route_name='save_payslip', renderer='string')
def save_payslip(request):
	auth_check_pass = Auth.check_user_session(request.session)
	if not auth_check_pass:
		raise exc.HTTPFound(request.route_url("login"))
	pay = request.POST['payslip_data']
	pay = json.loads(pay)
	dates = []
	for guard in pay:
		dates.append(pay[guard][0]['guard_shift_day'])

	Pay.save_payslip_data(pay,dates)
	return "abc"

@view_config(route_name='save_leave', renderer='string')
def save_leave(request):
	auth_check_pass = Auth.check_user_session(request.session)
	if not auth_check_pass:
		raise exc.HTTPFound(request.route_url("login"))
	pay = request.POST['payslip_data']
	pay = json.loads(pay)

	Pay.save_leave_data(pay)
	return "abc"