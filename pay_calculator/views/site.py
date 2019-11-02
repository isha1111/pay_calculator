from pyramid.view import view_config
from datetime import date
from dateutil import parser
from datetime import datetime 
from datetime import timedelta
import pyramid.httpexceptions as exc
from pay_calculator.models import site_model as Site
from pay_calculator.models import auth_model as Auth
import json
# import psycopg2

@view_config(route_name='site_add', renderer='../templates/site/site_add.mako')
def site_add(request):
	auth_check_pass = Auth.check_user_session(request.session)
	if not auth_check_pass:
		raise exc.HTTPFound(request.route_url("login"))
	return {'project':'PAY CALCULATOR','username':request.session['username']}

@view_config(route_name='site_list', renderer='string')
def site_list(request):
	auth_check_pass = Auth.check_user_session(request.session)
	if not auth_check_pass:
		raise exc.HTTPFound(request.route_url("login"))
	
	site_list = Site.get_list_of_site()

	return site_list

@view_config(route_name='site_save', renderer='../templates/site/site_save.mako')
def site_save(request):
	auth_check_pass = Auth.check_user_session(request.session)
	if not auth_check_pass:
		raise exc.HTTPFound(request.route_url("login"))
	sitename = request.params.get('sitename')
	notes = request.params.get('notes')
	try:
		Site.add_site_to_database(sitename,notes)
		result = 'Successfully saved'
	except:
		result = 'Something went wrong'

	return {'project':'PAY CALCULATOR','result':result,'username':request.session['username']}

