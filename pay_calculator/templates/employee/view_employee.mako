<%inherit file="../layout.mako"/>
<script src="https://cdnjs.cloudflare.com/ajax/libs/axios/0.18.0/axios.min.js" type="text/javascript"></script>
<link rel="stylesheet" type="text/css" href="/static/css/employee/employee_add.css">
<div class="title" id="title">
	${project}
</div>
<div class="submenu" >
	<ul style="list-style: none;">
		<li class="submenu_li"><a href="employee_add" >Add Employee</a> | </li>
		<li class="submenu_li"><a href="search_employee" >Search Employee</a> | </li>
		<li class="submenu_li"><a href="update_employee" >Update Employee</a> | </li> 
		<li class="submenu_li"><a href="delete_employee" >Delete Employee</a> | </li> 
	</ul>
</div>

<div class="title" id="employee_add_title">
	View Employee
</div>
<div id="container">
	<div id="form_div">
		<form id="employee_create_form">
		<!-- <div class="panel panel-default tab-page "> -->
			<div class="row">
				<div class="input">
					<label >Firstname</label>
					<input type="text" name="firstname" value="${emp_data[0]['firstname']}" disabled="disabled" style="background-color: lightgray">
				</div>
				<div class="input">
					<label >Lastname</label>
					<input type="text" name="lastname" value="${emp_data[0]['lastname']}" disabled="disabled" style="background-color: lightgray">
				</div>
			</div>
			
			<div class="row">
				<div class="input" >
						<label >Date of birth</label>
				<input type="date" name="dob" value="${emp_data[0]['date_of_birth']}" disabled="disabled" style="background-color: lightgray">
				</div>
				<div class="input">
					<label >Gender</label>
					<input type="text" name="gender" value="${emp_data[0]['gender']}"disabled="disabled" style="background-color: lightgray">
				</div>
			</div>
			
			<div class="row">
				<div class="input">
					<label >Phone</label>
					<input type="text" name="phone" value="${emp_data[0]['mobile']}" disabled="disabled" style="background-color: lightgray">
				</div>
				<div class="input">
					<label >Email</label>
					<input type="email" name="email" value="${emp_data[0]['email']}" disabled="disabled" style="background-color: lightgray">
				</div>
			</div>

			<div class="row">
				<div class="input">
					<label >Security License</label>
					<input type="text" name="security_license" disabled="disabled" style="background-color: lightgray" value="${emp_data[0]['security_license']}">
				</div>
				<div class="input">
					<label >Security License Expiry</label>
					<input type="text" name="security_license_expiry" disabled="disabled" style="background-color: lightgray" value="${emp_data[0]['security_license_expiry']}">
				</div>
			</div>
			
			<div class="row">
				<div class="input">
					<label >Award (Pay type)</label>
					<input type="text" name="awards" disabled="disabled" style="background-color: lightgray"  value="${emp_data[0]['award_type']}">
				</div>
				<div class="input">
					<label>Base rate</label>
					<input type="number" name="baserate" step="0.01" disabled="disabled" style="background-color: lightgray" value="${emp_data[0]['flat_rate']}">
				</div>
			</div>

			<div class="row">
				<div class="input">
					<label >BSB</label>
					<input type="text" name="bsb" disabled="disabled" style="background-color: lightgray" value="${emp_data[0]['bsb']}">
				</div>
				<div class="input">
					<label >Account</label>
					<input type="text" name="account" disabled="disabled" style="background-color: lightgray" value="${emp_data[0]['account']}">
				</div>
			</div>
			
			<div class="row">
				<div class="input">
					<label>Annual leave balance</label>
					<input type="number" name="annual_leave" step="0.01" disabled="disabled" style="background-color: lightgray" placeholder="0.00" value="${emp_data[0]['annual_leave']}">
				</div>
				<div class="input">
					<label>Sick leave balance</label>
					<input type="number" name="sick_leave" step="0.01" disabled="disabled" style="background-color: lightgray" placeholder="0.00" value="${emp_data[0]['sick_leave']}">
				</div>
				<div class="input" >
					<label>Long service leave balance</label>
					<input type="number" name="long_service_leave" step="0.01" disabled="disabled" style="background-color: lightgray" placeholder="0.00" value="${emp_data[0]['long_service_leave']}">
				</div>
				
			</div>

			<div class="row">
				<div class="input">
					<label>Notes</label>
					<textarea name="notes" disabled="disabled" style="background-color: lightgray" value="${emp_data[0]['notes']}"></textarea>
				</div>
			</div>
			
		<!-- </div>	 -->
		</form>


	
	<form method="post" id="form1" action="save_bulk_employee">
			<input type="text" name="guard_data" id="guard_data" style="display: none">
			<input type="submit" name="" style="display: none">
		</form>
	</div>

</div>
<script type="text/javascript">
	var app = new Vue({
		el: '#container',
		data: {

		},
		methods: {
			
		},
		mounted: function(){

		}
	})
</script>
