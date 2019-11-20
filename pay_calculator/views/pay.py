from pyramid.view import view_config
import pyramid.httpexceptions as exc
from pay_calculator.models import pay_model as Pay
from pay_calculator.models import auth_model as Auth
from pay_calculator.models import user_model as User
import pyramid.httpexceptions as exc
import json

@view_config(route_name='home', renderer='../templates/index.mako')
def my_view(request):
	auth_check_pass = Auth.check_user_session(request.session)
	if not auth_check_pass:
		raise exc.HTTPFound(request.route_url("login"))
	return {'project': 'PAY CALCULATOR','pay':'','username':request.session['username']}

@view_config(route_name='payslip', renderer='../templates/pay/payslip.mako')
def payslip(request):
	firstname = request.params.get('firstname').lower()
	start_date = request.params.get('start_date')
	end_date = request.params.get('end_date')
	# get pay and ytd data
	payslip_data = Pay.get_ytd_and_pay_data(firstname,start_date,end_date)
	return {'project': 'PAY CALCULATOR','pay':'','payslip_data':payslip_data}

@view_config(route_name='send_payslip', renderer='string')
def send_payslip(request):
	auth_check_pass = Auth.check_user_session(request.session)
	if not auth_check_pass:
		raise exc.HTTPFound(request.route_url("login"))
	firstname = request.params.get('firstname').lower()
	start_date = request.params.get('start_date')
	end_date = request.params.get('end_date')
	
	# get email for employee
	User.get_email_for_employee(firstname,start_date,end_date,request.response)
	return "Successfully sent email"

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
		data = Pay.calculate_jmd_eba_rate(roaster_data, state)
		return {'project': 'PAY CALCULATOR','pay':data[0],'pay_type':'jmd_eba','username':request.session['username'],'fortnight_start':data[1],'fortnight_end':data[2],'category':'security','state':state}

	if pay_type == 'jmd_eba3':
		data = Pay.calculate_jmd_eba3_rate(roaster_data, state)
		return {'project': 'PAY CALCULATOR','pay':data[0],'pay_type':'jmd_eba3','username':request.session['username'],'fortnight_start':data[1],'fortnight_end':data[2],'category':'security','state':state}

	if pay_type == 'jmd_eba2':
		data = Pay.calculate_jmd_eba2_rate(roaster_data, state)
		return {'project': 'PAY CALCULATOR','pay':data[0],'pay_type':'jmd_eba2','username':request.session['username'],'fortnight_start':data[1],'fortnight_end':data[2],'category':'security','state':state}

	if pay_type == 'jmd_eba1':
		data = Pay.calculate_jmd_eba1_rate(roaster_data, state)
		return {'project': 'PAY CALCULATOR','pay':data[0],'pay_type':'jmd_eba1','username':request.session['username'],'fortnight_start':data[1],'fortnight_end':data[2],'category':'security','state':state}

	if pay_type == 'awards':
		category = request.params.get('category')
		job_type = request.params.get('job_type')
		data = Pay.calculate_awards_rate(roaster_data, state,category,job_type)
		return {'project': 'PAY CALCULATOR','pay':data[0],'pay_type':'awards','username':request.session['username'],'fortnight_start':data[1],'fortnight_end':data[2],'category':category,'state':state}

	if pay_type == 'rss':
		data = Pay.calculate_rss_rate(roaster_data, state)
		return {'project': 'PAY CALCULATOR','pay':data[0],'pay_type':'rss','username':request.session['username'],'fortnight_start':data[1],'fortnight_end':data[2],'category':'security','state':state}

@view_config(route_name='save_payslip', renderer='string')
def save_payslip(request):
	auth_check_pass = Auth.check_user_session(request.session)
	if not auth_check_pass:
		raise exc.HTTPFound(request.route_url("login"))
	pay = request.POST['payslip_data']
	pay = json.loads(pay)
	fortnight_start = request.POST['fortnight_start']
	fortnight_end = request.POST['fortnight_end']

	Pay.save_payslip_data(pay,fortnight_start,fortnight_end)
	return "Saved successfully"

@view_config(route_name='save_leave', renderer='string')
def save_leave(request):
	auth_check_pass = Auth.check_user_session(request.session)
	if not auth_check_pass:
		raise exc.HTTPFound(request.route_url("login"))
	pay = request.POST['payslip_data']
	pay = json.loads(pay)

	Pay.save_leave_data(pay)
	return "Saved successfully"