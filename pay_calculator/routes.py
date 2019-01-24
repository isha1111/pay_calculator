def includeme(config):
	config.add_static_view('static', 'static', cache_max_age=3600)
	config.add_route('home', '/')
	config.add_route('calculate_payrate', '/calculate_payrate')
	config.add_route('employee_add','/employee_add')
