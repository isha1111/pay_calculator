<%inherit file="../layout.mako"/>
<script src="https://cdn.jsdelivr.net/npm/vue@2.5.17/dist/vue.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/xlsx/0.8.0/jszip.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/xlsx/0.8.0/xlsx.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/axios/0.18.0/axios.min.js" type="text/javascript"></script>
<link rel="stylesheet" type="text/css" href="/static/css/employee/employee_add.css">
<div class="title" id="title">
	${project}
</div>
<div class="title" id="employee_add_title">
	Search Employee 
</div>
<div id="container">
	<div id="form_div">
		<!-- <div class="panel panel-default tab-page "> -->
			<div class="row">
				<div class="input">
					<label class="required">Firstname</label>
					<input type="text" name="firstname" v-model="firstname">
				</div>
				<div class="input">
					<label >Lastname</label>
					<input type="text" name="lastname" v-model="lastname">
				</div>
			</div>

			<div class="row">
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
		<table >
			<tr>
				<th>Firstname</th>
				<th>Lastname</th>
				<th>Email</th>
				<th>Phone</th>
				<th>Security License</th>
			</tr>
			<tr v-for="row in search_result">
				<td>
					{{row["firstname"]}}
				</td>
				<td>
					{{row["lastname"]}}
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
			</tr>
		</table>
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
			'search_result': '' 
		},
		methods: {
			fetch_employee: function() {
				var url = '/fetch_employee?firstname='+this.firstname+'&lastname='+this.lastname+'&security_license='+this.security_license;
				axios.get(url).then(function(result){
					app.show_search_results = true;
					app.search_result = result["data"]
				})
			}
		},
		mounted: function(){

		}
	})
</script>