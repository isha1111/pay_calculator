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
		<li class="submenu_li"><a href="site_add" >Add Site</a> | </li>
		<li class="submenu_li"><a href="search_site" >Search Site</a> | </li>
		<li class="submenu_li"><a href="update_site" >Update Site</a> | </li> 
		<li class="submenu_li"><a href="delete_site" >Delete Site</a> | </li> 
	</ul>
</div>

<div class="title" id="employee_add_title">
	Add Site Information
</div>
<div id="container">
	
	<div id="form_div">
		<form action="/site_save" method="post"  id="site_create_form">
		<!-- <div class="panel panel-default tab-page "> -->
			<div class="row">
				<div class="input">
					<label class="required">Sitename</label>
					<input type="text" name="sitename">
				</div>
			</div>

			<div class="row">
				<div class="input">
					<label>Notes</label>
					<textarea placeholder="some notes" name="notes"></textarea>
				</div>
			</div>
			<div style="text-align: center;">
				<input type="submit" name="submit" id="site_button">
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
