<%inherit file="../layout.mako"/>
<script src="https://cdn.jsdelivr.net/npm/vue@2.5.17/dist/vue.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/xlsx/0.8.0/jszip.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/xlsx/0.8.0/xlsx.js"></script>
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
	Employee Information
</div>
<div id="container">
	<div id="mySidenav" class="sidenav">
		  <a class="closebtn" onclick="closeNav()">&times;</a>
		  <a href="#">Employee Add</a>
		  <a href="#">Employee Search</a>
		  <a href="#">Employee Update</a>
		  <a href="#">Employee Reminder</a>
	</div>
	<div id="panel">
		<div class="inline pointer options" @click="show_manual_emp_create">
			Create Employee Manually
		</div> or 
		<div class="inline pointer options" @click="show_file_upload">
			Upload Employee File Data
		</div>
	</div>
	<div id="form_div">
		<form action="/employee_save" method="post" v-show="employee_create" id="employee_create_form">
		<!-- <div class="panel panel-default tab-page "> -->
			<div class="row">
				<div class="input">
					<label class="required">Firstname</label>
					<input type="text" name="firstname">
				</div>
				<div class="input">
					<label >Lastname</label>
					<input type="text" name="lastname">
				</div>
			</div>
			
			<div class="row">
				<div class="input" >
						<label class="required">Date of birth</label>
				<input type="date" name="dob">
				</div>
				<div class="input">
					<label class="required">Gender</label>
					<select name="gender" >
						<option value="male">Male</option>
						<option value="female">Female</option>
						<option value="other">Other</option>
						<option value="undisclosed">Undisclosed</option>
					</select>
				</div>
			</div>
			
			<div class="row">
				<div class="input">
					<label class="required">Phone</label>
					<input type="text" name="phone">
				</div>
				<div class="input">
					<label class="required">Email</label>
					<input type="email" name="email">
				</div>
			</div>

			<div class="row">
				<div class="input">
					<label class="required">Security License</label>
					<input type="text" name="security_license">
				</div>
				<div class="input">
					<label class="required">Security License Expiry</label>
					<input type="date" name="security_license_expiry">
				</div>
			</div>
			
			<div class="row">
				<div class="input">
					<label class="required ">Award (Pay type)</label>
					<select name="awards">
						<option value="jmd_eba">JMD EBA</option>
						<option value="awards">Awards</option>
						<option value="rss">RSS</option>
						<option value="flat_rate">Flat rate</option>
						<option value="other">Other</option>
					</select>
				</div>
				<div class="input">
					<label>Base rate</label>
					<input type="number" name="baserate" step="0.01">
				</div>
			</div>

			<div class="row">
				<div class="input">
					<label class="required ">BSB</label>
					<input type="text" name="bsb">
				</div>
				<div class="input">
					<label class="required">Account</label>
					<input type="text" name="account" >
				</div>
			</div>
			
			<div class="row">
				<div class="input">
					<label>Annual leave balance</label>
					<input type="number" name="annual_leave" step="0.01" disabled="disabled" placeholder="0.00">
				</div>
				<div class="input">
					<label>Sick leave balance</label>
					<input type="number" name="sick_leave" step="0.01" disabled="disabled" placeholder="0.00">
				</div>
				<div class="input" >
					<label>Long service leave balance</label>
					<input type="number" name="long_service_leave" step="0.01" disabled="disabled" placeholder="0.00">
				</div>
				
			</div>

			<div class="row">
				<div class="input">
					<label>Notes</label>
					<textarea placeholder="has CPR cert." name="notes"></textarea>
				</div>
			</div>
			<div style="text-align: center;">
				<input type="submit" name="submit" id="employee_button">
			</div>
			
		<!-- </div>	 -->
		</form>


	<form v-show="employee_file_upload" id="employee_upload_form">
		<span style="margin-left: 5em; margin-right: 1em">UPLOAD EMPLOYEE DATA FILE:</span>
		<input type="file" name="employee_file" v-on:change="xls_to_json($event)"><br>
		<br>
		<input style="margin-left: 19em; margin-right: 1em" type="button" value="Upload Employee" @click="save_employee_from_sheet">
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
			'employee_file_upload' : false,
			'employee_create' : true,
			'employee_uploaded_data' : ''
		},
		methods: {
			show_manual_emp_create: function(){
				var self = this;
				self.employee_file_upload = false;
				self.employee_create = true;
			},
			show_file_upload: function(){
				var self = this;
				self.employee_file_upload = true;
				self.employee_create = false;
			},
			xls_to_json: function(oEvent) {
				// Get The File From The Input
				var oFile = oEvent.target.files[0];
				var sFilename = oFile.name;
				// Create A File Reader HTML5
				var reader = new FileReader();
				var something = [];

				// Ready The Event For When A File Gets Selected
				reader.onload = function(e) {
				    var data = e.target.result;
				    var cfb = XLSX.read(data, {type: 'binary'});
				    cfb.SheetNames.forEach(function(sheetName) {
				        // Obtain The Current Row As CSV
				        var sCSV = XLS.utils.make_csv(cfb.Sheets[sheetName], {FS:"\t"});   
				        app.employee_uploaded_data = sCSV;
				    });
				};

				// Tell JS To Start Reading The File.. You could delay this if desired
				reader.readAsBinaryString(oFile);
			},
			save_employee_from_sheet: function(){
				var all_data = app.employee_uploaded_data;
		    	document.getElementById("guard_data").value = JSON.stringify(all_data);
		    	$("#form1").submit();
			}
		},
		mounted: function(){

		}
	})
</script>
