<%inherit file="../layout.mako"/>
<script src="https://cdn.jsdelivr.net/npm/vue@2.5.17/dist/vue.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/xlsx/0.8.0/jszip.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/xlsx/0.8.0/xlsx.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/axios/0.18.0/axios.min.js" type="text/javascript"></script>
<div class="title" id="title">
	${project}
</div>
<div class="title" id="employee_add_title">
	Send Reminder to Guard
</div>

<div id="container">
	<div id="form_div">
		<button @click="addFile">
		    Add new file upload
		</button>
		<button @click="removeFile">
		    Remove file upload
		</button>
		<div v-for="num in files">
			<input v-bind:id="num" type=file  name="files[]" v-on:change='filePicked($event)'>
		</div>

		<input type="button" value="Send Email" @click="organize_data">

		<form method="post" id="form1" action="send_email_to_guards">
			<input type="text" name="roaster_data" id="actual_data" style="display: none">
			<input type="submit" name="" style="display: none">
		</form>
		

	</div>

</div>

<script>
	var app = new Vue({
		el: '#container',
		data: {
			'num_of_sheets' : [1,2,3,4,5,6,7,8,9,10,11,12,13,14],
			'user_num_of_sheets':0,
			'files' : [],
			'current_num': 0,
			'all_data': {}
		},
		methods: {
			addFile: function () {
				this.user_num_of_sheets = this.user_num_of_sheets + 1;
		        this.files.push(this.user_num_of_sheets);
		    },
		    removeFile: function () {
		    	this.user_num_of_sheets = this.user_num_of_sheets - 1;
		    	var last_file = this.files[this.files.length - 1]
		    	delete this.all_data[last_file.toString()]
		        this.files.pop();

		    },
		    organize_data: function(){
		    	var roaster_data = this.all_data
		    	document.getElementById("actual_data").value = JSON.stringify(roaster_data);
		    	$("#form1").submit();
		    // 	axios.post('/send_email_to_guards', {
				  //   data: JSON.stringify(roaster_data),
				  //   contentType: 'application/json',
				  // })
				  // .then(function (response) {
				  //   console.log('done');
				  // })
				  // .catch(function (error) {
				  //   console.log(error);
				  // });

				
		    },
		    save_file_data: function(){

		    },
		    filePicked: function(oEvent) {
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
				        app.all_data[oEvent.target.id] = sCSV;
				    });
				};

				// Tell JS To Start Reading The File.. You could delay this if desired
				reader.readAsBinaryString(oFile);
			}
		},
		mounted: function(){
			this.addFile()
		}
	})

    

	// document.getElementById('upload').addEventListener('change', filePicked, false);
</script>
