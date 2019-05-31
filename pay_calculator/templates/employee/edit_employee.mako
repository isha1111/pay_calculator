<%inherit file="../layout.mako"/>
<script src="https://cdn.jsdelivr.net/npm/vue@2.5.17/dist/vue.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/axios/0.18.0/axios.min.js" type="text/javascript"></script>
<link rel="stylesheet" type="text/css" href="/static/css/employee/employee_add.css">
<script src="https://cdnjs.cloudflare.com/ajax/libs/axios/0.18.0/axios.min.js" type="text/javascript"></script>
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
	Edit Employee
</div>
<div id="container">
	<div id="form_div">
		<!-- <div class="panel panel-default tab-page "> -->
			<div class="row">
				<input type="hidden" name="emp_id" value="${emp_data[0]['employee_id']}" id="emp_id">
				<div class="input">
					<label >Firstname</label>
					<input type="text" name="firstname" value="${emp_data[0]['firstname']}" id="firstname">
				</div>
				<div class="input">
					<label >Lastname</label>
					<input type="text" name="lastname" value="${emp_data[0]['lastname']}" id="lastname">
				</div>
			</div>
			
			<div class="row">
				<div class="input" >
						<label >Date of birth</label>
				<input type="date" name="dob" value="${emp_data[0]['date_of_birth']}" id="dob">
				</div>
				<div class="input">
					<label >Gender</label>
					<input type="text" name="gender" value="${emp_data[0]['gender']}" id="gender">
				</div>
			</div>
			
			<div class="row">
				<div class="input">
					<label >Phone</label>
					<input type="text" name="phone" value="${emp_data[0]['mobile']}" id="phone">
				</div>
				<div class="input">
					<label >Email</label>
					<input type="email" name="email" value="${emp_data[0]['email']}" id="email">
				</div>
			</div>

			<div class="row">
				<div class="input">
					<label >Security License</label>
					<input type="text" name="security_license" value="${emp_data[0]['security_license']}" id="security_license">
				</div>
				<div class="input">
					<label >Security License Expiry</label>
					<input type="text" name="security_license_expiry" value="${emp_data[0]['security_license_expiry']}" id="security_license_expiry">
				</div>
			</div>
			
			<div class="row">
				<div class="input">
					<label >Award (Pay type)</label>
					<input type="text" name="awards"  value="${emp_data[0]['award_type']}" id="award">
				</div>
				<div class="input">
					<label>Base rate</label>
					<input type="number" name="baserate" step="0.01" value="${emp_data[0]['flat_rate']}" id="baserate">
				</div>
			</div>

			<div class="row">
				<div class="input">
					<label >BSB</label>
					<input type="text" name="bsb" value="${emp_data[0]['bsb']}" id="bsb">
				</div>
				<div class="input">
					<label >Account</label>
					<input type="text" name="account" value="${emp_data[0]['account']}" id="account">
				</div>
			</div>
			
			<div class="row">
				<div class="input">
					<label>Annual leave balance</label>
					<input type="number" name="annual_leave" step="0.01" placeholder="0.00" value="${emp_data[0]['annual_leave']}" id="annual_leave">
				</div>
				<div class="input">
					<label>Sick leave balance</label>
					<input type="number" name="sick_leave" step="0.01" placeholder="0.00" value="${emp_data[0]['sick_leave']}" id="sick_leave">
				</div>
				<div class="input" >
					<label>Long service leave balance</label>
					<input type="number" name="long_service_leave" step="0.01" placeholder="0.00" value="${emp_data[0]['long_service_leave']}" id="long_service_leave">
				</div>
				
			</div>

			<div class="row">
				<div class="input">
					<label>Notes</label>
					<textarea name="notes" value="${emp_data[0]['notes']}" id="notes"></textarea>
				</div>
			</div>
			<div style="text-align: center;">
				<input type="submit" name="submit" id="employee_button" @click="update_employee()">
			</div>
			
		<!-- </div>	 -->

</div>
</div>
<script type="text/javascript">
	var app = new Vue({
		el: '#container',
		data: {

		},
		methods: {
			update_employee: function(){
				var bodyFormData = new FormData();
				bodyFormData.append('emp_id', $("#emp_id").val());
				bodyFormData.append('firstname', $("#firstname").val());
				bodyFormData.append('lastname', $("#lastname").val());
				bodyFormData.append('dob', $("#dob").val());
				bodyFormData.append('gender', $("#gender").val());
				bodyFormData.append('phone', $("#phone").val());
				bodyFormData.append('email', $("#email").val());
				bodyFormData.append('security_license', $("#security_license").val());
				bodyFormData.append('security_license_expiry', $("#security_license_expiry").val());
				bodyFormData.append('award', $("#award").val());
				bodyFormData.append('baserate', $("#baserate").val());
				bodyFormData.append('bsb', $("#bsb").val());
				bodyFormData.append('account', $("#account").val());
				bodyFormData.append('annual_leave', $("#annual_leave").val());
				bodyFormData.append('sick_leave', $("#sick_leave").val());
				bodyFormData.append('long_service_leave', $("#long_service_leave").val());
				bodyFormData.append('notes', $("#notes").val());

				axios.post('/save_updated_employee', bodyFormData)
				  .then(function (response) {
				    alert(response.data)
				  })
				  .catch(function (error) {
				    console.log(error);
				  });
			}
		},
		mounted: function(){

		}
	})
</script>
