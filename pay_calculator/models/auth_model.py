def check_user_session(session_var):
	if ('username' not in session_var):
		return False
	else:
		if session_var['username'] == '':
			return False
	return True