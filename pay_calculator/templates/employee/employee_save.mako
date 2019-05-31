<%inherit file="../layout.mako"/>
<link rel="stylesheet" type="text/css" href="/static/css/employee/employee_add.css">
<div class="title" id="title">
	${project}
</div>
<div class="submenu" >
	<ul style="list-style: none;">
		<li class="submenu_li"><a href="employee_add" >Add Employee</a> | </li>
		<li class="submenu_li"><a href="search_employee" >Search Employee</a> | </li>
		<li class="submenu_li"><a href="update_employee" >Update Employee</a> | </li> | 
		<li class="submenu_li"><a href="delete_employee" >Delete Employee</a> | </li> 
	</ul>
</div>
<div style="text-align: center;">
	${result}
</div>
