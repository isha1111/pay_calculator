<%inherit file="../layout.mako"/>
<link rel="stylesheet" type="text/css" href="/static/css/employee/employee_add.css">
<div class="title" id="title">
	${project}
</div>
<div class="submenu" >
	<ul style="list-style: none;">
		<li class="submenu_li"><a href="site_add" >Add Site</a> | </li>
		<li class="submenu_li"><a href="search_site" >Search Site</a> | </li>
		<li class="submenu_li"><a href="update_site" >Update Site</a> | </li> 
		<li class="submenu_li"><a href="delete_site" >Delete Site</a> | </li> 
	</ul>
</div>
<div style="text-align: center;">
	${result}
</div>
