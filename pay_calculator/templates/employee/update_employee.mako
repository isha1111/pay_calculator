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
		<li class="submenu_li"><a href="home" >Pay Calculator</a> | </li> 
	</ul>
</div>
<div class="title" id="employee_add_title">
	Search and Update Employee 
</div>
<div id="container">
	<div id="form_div">
		<!-- <div class="panel panel-default tab-page "> -->
			<div class="row">
				<div class="input">
					<label>Fullname</label>
					<input type="text" name="firstname" v-model="firstname">
				</div>
				<div class="input">
					<label>Security License</label>
					<input type="text" name="security_license" v-model="security_license">
				</div>
			</div>
			
			<div style="text-align: center;">
				<input type="button" value="Search" @click='fetch_employee'>
			</div>
			
	</div>	

	<div id="search_div" v-if="show_search_results">
		Search Results
		<br>
		<table >
			<tr>
				<th>Firstname</th>
				<th>Email</th>
				<th>Phone</th>
				<th>Security License</th>
				<th>Update</th>
			</tr>
			<tr v-for="row in search_result">
				<td>
					{{row["firstname"]}}
				</td>
				<td>
					{{row["email"]}}
				</td>
				<td>
					{{row["phone"]}}
				</td>
				<td>
					{{row["security_license"]}}
				</td>
				<td style="cursor: pointer;color:blue;">
					<a :href="'/edit_employee?emp_id='+row['employee_id']" target="_blank">edit
				</td>
			</tr>
		</table>
	</div>

	<div id="no_result_div" v-if="show_no_result_found">
		No results found
	</div>

</div>
<script type="text/javascript">
	var app = new Vue({
		el: '#container',
		data: {
			'security_license': '',
			'firstname': '',
			'lastname': '',
			'show_search_results': false,
			'search_result': '',
			'show_no_result_found': false
		},
		methods: {
			fetch_employee: function() {
				var url = '/fetch_employee?firstname='+this.firstname+'&security_license='+this.security_license;
				axios.get(url).then(function(result){
					if(result["data"].length != 0){
						app.show_search_results = true;
						app.search_result = result["data"];
						app.show_no_result_found = false;
					}
					else{
						app.show_no_result_found = true;
						app.show_search_results = false;
					}
				})
			}
		},
		mounted: function(){

		}
	})
</script>
