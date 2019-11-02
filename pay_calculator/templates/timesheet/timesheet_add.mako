<%inherit file="../layout.mako"/>
<script src="https://cdnjs.cloudflare.com/ajax/libs/xlsx/0.8.0/jszip.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/xlsx/0.8.0/xlsx.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/axios/0.18.0/axios.min.js" type="text/javascript"></script>
<link rel="stylesheet" type="text/css" href="/static/css/employee/employee_add.css">
<div class="title" id="title">
	${project}
</div>
<div class="submenu" >
	<ul style="list-style: none;">
		<li class="submenu_li"><a href="timesheet_add" >Add Timesheet</a> | </li>
		<li class="submenu_li"><a href="search_timesheet" >Search Timesheet</a> | </li>
		<li class="submenu_li"><a href="update_timesheet" >Update Timesheet</a> | </li> 
		<li class="submenu_li"><a href="delete_timesheet" >Delete Timesheet</a> | </li> 
	</ul>
</div>

<div class="title" id="employee_add_title">
	Add Timesheet Information
</div>
<div id="container">
	
	<div id="form_div">
		<form action="/timesheet_save" method="post"  id="timesheet_create_form">
		<!-- <div class="panel panel-default tab-page "> -->
			<div class="row">
				<div class="input" >
					<label class="required">Date</label>
					<input type="date" name="shift_date" required>
				</div>
			</div>
			<div class="row">
				<div class="input" >
					<label class="required">Guard Name</label>
					<input type="text" name="guard_name" required>
				</div>
			</div>
			<div class="row">
				<div class="input" >
					<label class="required">Site Name</label>
					<select name="site_name" required>
						<option>
							% for site in sites:
							${site}
							% endfor
						</option>
					</select>
				</div>
			</div>
			<div class="row">
				<div class="input" >
					<label class="required">Start time</label>
					<input type="time" name="start_time" required>
				</div>
				<div class="input" >
					<label class="required">End time</label>
					<input type="time" name="end_time" required>
				</div>
			</div>

			<div class="row">
				<div class="input">
					<label class="required">Payable hours</label>
					<input type="number" name="payable_hours" required>
				</div>
			</div>
			<div style="text-align: center;">
				<input type="submit" name="submit" value="save" id="site_button">
			</div>
			
		<!-- </div>	 -->
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
