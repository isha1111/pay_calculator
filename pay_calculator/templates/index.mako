<%inherit file="layout.mako"/>
<style type="text/css">
	.submenu {
	    text-align: center;
	}

	.submenu_li {
	    display: inline;
	}

	.submenu_li a {
	    color: black;
	}

	.submenu_li:hover {
	    color: blue;
	    cursor: pointer;
	}
</style>
<div class="title" id="title">
	${project}
</div>
<div class="submenu" >
	<ul style="list-style: none;">
		<li class="submenu_li"><a href="employee_add" >Add Employee</a> | </li>
		<li class="submenu_li"><a href="search_employee" >Search Employee</a> | </li>
		<li class="submenu_li"><a href="update_employee" >Update Employee</a> | </li> 
		<li class="submenu_li"><a href="delete_employee" >Delete Employee</a> | </li> 
		<li class="submenu_li"><a href="home" >Pay Calculator</a> | </li> 
	</ul>
</div>
<div class="hidden" id="calculated_data"></div>
<div id="instructions" class="center">
	<span class="warning">PLEASE NOTE FOLLOWING:</span></br>
	<div id="instruction-points">
		The <b>excel sheet headers should have extra column 'level' (with information on guard level eg 1,2..)</b> and the other columns should be same as the one generated from Ento (including header - Officer full name, Published start date, Published start, Published end, Published actual hours, Published location name and so on ...)</br>
	</div>
</div>
<div class="form">
	<form enctype="multipart/form-data" action="/calculate_payrate" method="post">
		<label>State</label>
		<select name="state">
			<option value="NSW">NSW</option>
			<option value="VIC">VIC</option>
			<option value="WA">WA</option>
			<option value="ACT">ACT</option>
			<option value="QLD">QLD</option>
			<option value="SA">SA</option>
		</select></br>
		</br>
		<label>Pay Type</label>
		<select name="pay_type">
			<option value="jmd_eba">JMD EBA</option>
			<option value="awards">awards</option>
			<option value="rss">RSS</option>
		</select></br>
		<label class="label">PLEASE UPLOAD FILE HERE:</label>
		<input type="file" id="roaster_file"  name="roaster_data"></br>
		<input type="submit" id="calculate_input" name="submit" value="CALCULATE PAY" >
	</form>
</div>


