from pyramid.view import view_config
from datetime import date
from dateutil import parser
from datetime import datetime 
from datetime import timedelta

@view_config(route_name='employee_add', renderer='../templates/employee_add.mako')
def employee_add(request):
	return True