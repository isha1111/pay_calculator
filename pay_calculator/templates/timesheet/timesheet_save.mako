<%inherit file="../layout.mako"/>
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
<div style="text-align: center;">
	${result}
</div>
