<%inherit file="../layout.mako"/>
<script src="https://cdn.jsdelivr.net/npm/vue@2.5.17/dist/vue.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/axios/0.18.0/axios.min.js" type="text/javascript"></script>
<link rel="stylesheet" type="text/css" href="/static/css/employee/employee_add.css">

<%
import json
%>

<div class="title" id="title">
	${project}
</div>

<div class="title" id="employee_add_title">
	User Login 
</div>

<div id="container">
	<div id="form_div">
		<form method="post" action="/log_user">
			<div class="row">
				<div class="input">
					<label class="required">Email/Username</label>
					<input type="email" name="email" v-model="email" required="true">
				</div>
				<div class="input">
					<label class="required">Password</label>
					<input type="password" name="password" required="true">
				</div>
				
			</div>
			
			<div style="text-align: center;">
				<input type="submit" value="Login">
			</div>
		</form>
	</div>
</div>
