from pyramid.view import view_config
from datetime import date
from dateutil import parser
from datetime import datetime 
from datetime import timedelta
import pyramid.httpexceptions as exc
from pay_calculator.models import timesheet_model as Timesheet
from pay_calculator.models import site_model as Site
from pay_calculator.models import auth_model as Auth
import json
# import psycopg2

@view_config(route_name='timesheet_add', renderer='../templates/timesheet/timesheet_add.mako')
def timesheet_add(request):
	auth_check_pass = Auth.check_user_session(request.session)
	if not auth_check_pass:
		raise exc.HTTPFound(request.route_url("login"))
	sites = Site.get_list_of_site()
	return {'project':'PAY CALCULATOR','username':request.session['username'],'sites':sites}

@view_config(route_name='timesheet_save', renderer='../templates/timesheet/timesheet_save.mako')
def timesheet_save(request):
	auth_check_pass = Auth.check_user_session(request.session)
	if not auth_check_pass:
		raise exc.HTTPFound(request.route_url("login"))
	shift_date = request.params.get('shift_date')
	guard_name = request.params.get('guard_name')
	site_name = request.params.get('site_name')
	start_time = request.params.get('start_time')
	end_time = request.params.get('end_time')
	payable_hours = request.params.get('payable_hours')
	# try:
	Timesheet.add_timesheet_to_database(shift_date,guard_name,site_name,start_time,end_time,payable_hours)
	result = 'Successfully saved'
	# except:
	# 	result = 'Something went wrong'

	return {'project':'PAY CALCULATOR','result':result,'username':request.session['username']}