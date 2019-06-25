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
	Regsiter User 
</div>

<div id="container">
	<div id="confirmation" style="text-align: center;">
		{{ confirmation_msg }}
	</div>
	<div id="form_div">
		<form method="post" action="/register">
			<div class="row">
				<div class="input">
					<label class="required">Fullname</label>
					<input type="text" name="firstname" v-model="firstname" required="true">
				</div>
				<div class="input">
					<label class="required">Email</label>
					<input type="email" name="email" v-model="email" required="true">
				</div>
				<div class="input">
					<label class="required">Password</label>
					<input type="password" name="password" required="true">
				</div>
				<div class="input">
					<label class="required">Confirm password</label>
					<input type="password" name="password2" required="true">
				</div>
				
			</div>
			
			<div style="text-align: center;">
				<input type="submit" value="Regsiter">
			</div>
		</form>
		<div style="text-align: center;">
			<span style="font-size: .75em">OR</span>
		</div>
		<div style="text-align: center;">
			<button> <a href="/login" style="text-decoration: none;">Login</a> </button>
		</div>
		<!-- <div class="panel panel-default tab-page "> -->
	</div>	

</div>

<script type="text/javascript">
	var app = new Vue({
		el: '#container',
		data: {
			'firstname': ${json.dumps(firstname) | n},
			'email': ${json.dumps(email) | n},
			'confirmation_msg': ${json.dumps(confirmation_msg) | n}
		},
		methods: {
			
		},
		mounted: function(){

		}
	})
</script>