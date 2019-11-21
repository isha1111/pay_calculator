// function csv_reader(){
//   var fileToLoad = document.getElementById("roaster_file").files[0];
//   var fileReader = new FileReader();
//   fileReader.onload = function(fileLoadedEvent){
//       var textFromFileLoaded = fileLoadedEvent.target.result;
//       $.ajax({
// 		  url: "/calculate_payrate",
// 		  type: "get", //send it through get method
// 		  data: { 
// 		    roaster_data : textFromFileLoaded
// 		  },
// 		  success: function(response) {
// 		  	document.getElementById("download_span").style.display = "block";
// 		  	$("#calculated_data").html(JSON.stringify(response));
// 		    DrawTable_eba(response);
// 		  },
// 		  error: function(xhr) {
// 		    //Do Something to handle error
// 		  }
// 		});
//   };

//   fileReader.readAsText(fileToLoad, "UTF-8");
// }

function download_data(){
	var pay_type = $("#pay_type").html();
	if(pay_type == 'jmd_eba'){
		ConvertToCSV_eba();
	}
	if(pay_type == 'jmd_eba1'){
		ConvertToCSV_eba1();
	}
	if(pay_type == 'jmd_eba2'){
		ConvertToCSV_eba2();
	}
	if(pay_type == 'jmd_eba3'){
		ConvertToCSV_eba3();
	}
	if(pay_type == 'awards'){
		ConvertToCSV_awards()
	}
	if(pay_type == 'rss'){
		ConvertToCSV_rss()
	}
}

function generate_and_save_payslip(){
	$('#loading').show();
	var pay_data = $( "#hidden_pay" ).html();
	var start_date = $( "#hidden_start_date" ).html().replace(/\n/g, '').trim();
	var end_date = $( "#hidden_end_date" ).html().replace(/\n/g, '').trim();
	var request = $.ajax({
	    url: 'save_payslip',
	    type: 'POST',
	    data: { payslip_data: pay_data, fortnight_start:start_date, fortnight_end:end_date} 
	   	});

	request.done(function(data) {
	      // your success code here
	      $('#loading').hide();
	      alert('Sucessfully generated');
	});

	request.fail(function(jqXHR, textStatus) {
	      // your failure code here
	      $('#loading').hide();
	      alert('Error encountered');
	});
}


function generate_and_save_leave(){
	$('#loading').show();
	var pay_data = $( "#hidden_pay" ).html();
	var request = $.ajax({
	    url: 'save_leave',
	    type: 'POST',
	    data: { payslip_data: pay_data} 
	   	});

	request.done(function(data) {
	      // your success code here
	      $('#loading').hide();
	      alert('Sucessfully generated');
	});

	request.fail(function(jqXHR, textStatus) {
	      // your failure code here
	      $('#loading').hide();
	      alert('Error encountered');
	});
}


function ConvertToCSV_rss() {
		var pay_data = $( "#hidden_pay" ).html();
       	var file_data = JSON.parse(pay_data);
        var str = '';
        var header = 'name,weekday,weekend,leave hours,total_amount\r\n';
        str += header;
        for (var i = 0; i < Object.keys(file_data).length; i++) {
            var line = '';
            var guard_name = Object.keys(file_data)[i];
            line += guard_name.toUpperCase() + ","; 
            line += file_data[guard_name][0]["weekday_hours"] +",";
            line += file_data[guard_name][0]["weekend_hours"] +",";
            line += file_data[guard_name][0]["leave_hours"] + "," ;
            line += file_data[guard_name][0]["total_amount"] ;

            str += line + '\r\n';
        }

		var hiddenElement = document.createElement('a');

		hiddenElement.href = 'data:attachment/text,' + encodeURI(str);
		hiddenElement.target = '_blank';
		hiddenElement.download = 'calculated_payrate.csv';
		hiddenElement.click();
    }

function ConvertToCSV_awards() {
		var pay_data = $( "#hidden_pay" ).html();
       	var file_data = JSON.parse(pay_data);
        var str = '';
        var header = 'name,hourly,saturday,sunday,public holiday,night span,leave hours,total_amount\r\n';
        str += header;
        for (var i = 0; i < Object.keys(file_data).length; i++) {
            var line = '';
            var guard_name = Object.keys(file_data)[i];
            line += guard_name.toUpperCase() + ","; 
            line += file_data[guard_name][0]["hourly_hours"] +",";
            line += file_data[guard_name][0]["saturday_hours"] +",";
            line += file_data[guard_name][0]["sunday_hours"] +",";
            line += file_data[guard_name][0]["public_holiday_hours"] +",";
            line += file_data[guard_name][0]["night_span_hours"] +",";
            line += file_data[guard_name][0]["leave_hours"] + "," ;
            line += file_data[guard_name][0]["total_amount"] ;

            str += line + '\r\n';
        }

		var hiddenElement = document.createElement('a');

		hiddenElement.href = 'data:attachment/text,' + encodeURI(str);
		hiddenElement.target = '_blank';
		hiddenElement.download = 'calculated_payrate.csv';
		hiddenElement.click();
    }

function ConvertToCSV_eba() {
		var pay_data = $( "#hidden_pay" ).html();
       	var file_data = JSON.parse(pay_data);
        var str = '';
        var header = 'name,20.21,24.68,21.11,26.68,25.12,50.53,leave hours,gross pay,tax,net pay\r\n';
        str += header;
        for (var i = 0; i < Object.keys(file_data).length; i++) {
            var line = '';
            var guard_name = Object.keys(file_data)[i];
            line += guard_name.toUpperCase() + ","; 
            line += file_data[guard_name][0]["weekday_no_rotating_rate"] +",";
            line += file_data[guard_name][0]["weeknight_no_rotating_rate"] +",";
            line += file_data[guard_name][0]["weekday_and_weeknight_rate"] +",";
            line += file_data[guard_name][0]["weeknight_and_weekend_rotating_rate"] +",";
            line += file_data[guard_name][0]["weekday_and_weeknight_and_weekend_rotating_rate"] +",";
            line += file_data[guard_name][0]["public_holiday_hours"] + "," ;
            line += file_data[guard_name][0]["leave_rate"] + "," ;
            line += (file_data[guard_name][0]["total_amount"]).toFixed(2) + "," ;
            line += (file_data[guard_name][0]["tax"]).toFixed(2)+ "," ;
            line += (file_data[guard_name][0]["net_pay"]).toFixed(2) ;

            str += line + '\r\n';
        }

		var hiddenElement = document.createElement('a');

		hiddenElement.href = 'data:attachment/text,' + encodeURI(str);
		hiddenElement.target = '_blank';
		hiddenElement.download = 'calculated_payrate.csv';
		hiddenElement.click();
    }

function ConvertToCSV_eba1() {
		var pay_data = $( "#hidden_pay" ).html();
       	var file_data = JSON.parse(pay_data);
        var str = '';
        var header = 'name,27.00,27.90,leave hours,gross pay,tax,net pay\r\n';
        str += header;
        for (var i = 0; i < Object.keys(file_data).length; i++) {
            var line = '';
            var guard_name = Object.keys(file_data)[i];
            line += guard_name.toUpperCase() + ","; 
            line += file_data[guard_name][0]["day_hours"] +",";
            line += file_data[guard_name][0]["night_hours"] +",";
            line += file_data[guard_name][0]["leave_hours"] +",";
            line += (file_data[guard_name][0]["total_amount"]).toFixed(2) + "," ;
            line += (file_data[guard_name][0]["tax"]).toFixed(2) + "," ;
            line += (file_data[guard_name][0]["net_pay"]).toFixed(2) ;

            str += line + '\r\n';
        }

		var hiddenElement = document.createElement('a');

		hiddenElement.href = 'data:attachment/text,' + encodeURI(str);
		hiddenElement.target = '_blank';
		hiddenElement.download = 'calculated_payrate.csv';
		hiddenElement.click();
    }

function ConvertToCSV_eba2() {
		var pay_data = $( "#hidden_pay" ).html();
       	var file_data = JSON.parse(pay_data);
        var str = '';
        var header = 'name,26.00,leave hours,gross pay,tax,net pay\r\n';
        str += header;
        for (var i = 0; i < Object.keys(file_data).length; i++) {
            var line = '';
            var guard_name = Object.keys(file_data)[i];
            line += guard_name.toUpperCase() + ","; 
            line += file_data[guard_name][0]["hours"] +",";
            line += file_data[guard_name][0]["leave_hours"] +",";
            line += (file_data[guard_name][0]["total_amount"]).toFixed(2) + "," ;
            line += (file_data[guard_name][0]["tax"]).toFixed(2) + "," ;
            line += (file_data[guard_name][0]["net_pay"]).toFixed(2) ;

            str += line + '\r\n';
        }

		var hiddenElement = document.createElement('a');

		hiddenElement.href = 'data:attachment/text,' + encodeURI(str);
		hiddenElement.target = '_blank';
		hiddenElement.download = 'calculated_payrate.csv';
		hiddenElement.click();
    }

function ConvertToCSV_eba3() {
		var pay_data = $( "#hidden_pay" ).html();
       	var file_data = JSON.parse(pay_data);
        var str = '';
        var header = 'name,26.65,leave hours,gross pay,tax,net pay\r\n';
        str += header;
        for (var i = 0; i < Object.keys(file_data).length; i++) {
            var line = '';
            var guard_name = Object.keys(file_data)[i];
            line += guard_name.toUpperCase() + ","; 
            line += file_data[guard_name][0]["hours"] +",";
            line += file_data[guard_name][0]["leave_hours"] +",";
            line += (file_data[guard_name][0]["total_amount"]).toFixed(2) + "," ;
            line += (file_data[guard_name][0]["tax"]).toFixed(2) + "," ;
            line += (file_data[guard_name][0]["net_pay"]).toFixed(2) ;

            str += line + '\r\n';
        }

		var hiddenElement = document.createElement('a');

		hiddenElement.href = 'data:attachment/text,' + encodeURI(str);
		hiddenElement.target = '_blank';
		hiddenElement.download = 'calculated_payrate.csv';
		hiddenElement.click();
    }


function sendPayslip(guard_name,fortnight_date,fortnight_end){
	var request = $.ajax({
	    url: 'send_payslip',
	    type: 'GET',
	    data: { firstname: guard_name, start_date: fortnight_date.trim(), end_date: fortnight_end.trim()} 
	   	});

	request.done(function(data) {
	      // your success code here
	      $('#loading').hide();
	      alert('Sucessfully sent');
	});

	request.fail(function(jqXHR, textStatus) {
	      // your failure code here
	      $('#loading').hide();
	      alert('Error encountered');
	});
}

function DrawTable_eba(file_data,start_date,end_date,var_state) {
	var file_data = JSON.parse(file_data);
	var str = "<table id='pay_table'><thead><tr><td>Guard Name</td><td>State</td><td>21.89</td><td>26.19</td><td>22.37</td><td>28.31</td><td>26.65</td><td>54.68</td><td>Leave hours</td><td>Gross Pay</td><td>Tax</td><td>Net Pay</td><td>Payslip</td></tr></thead><tbody>";
	
	for (var i = 0; i < Object.keys(file_data).length; i++) {
			var guard_name = Object.keys(file_data)[i];
			str += "<tr><td>"+guard_name.toUpperCase()+"</td><td>"+var_state+"</td><td>"+file_data[guard_name][0]['weekday_no_rotating_rate']+"</td><td>"+file_data[guard_name][0]["weeknight_no_rotating_rate"]+"</td><td>"+file_data[guard_name][0]["weekday_and_weeknight_rate"]+"</td><td>"+file_data[guard_name][0]["weeknight_and_weekend_rotating_rate"].toFixed(2)+"</td><td>"+file_data[guard_name][0]["weekday_and_weeknight_and_weekend_rotating_rate"].toFixed(2)+"</td><td>"+file_data[guard_name][0]["public_holiday_hours"].toFixed(2)+"</td><td>"+file_data[guard_name][0]["leave_rate"]+"</td><td>"+parseFloat(file_data[guard_name][0]["total_amount"]).toFixed(2)+"</td><td>"+parseFloat(file_data[guard_name][0]["tax"]).toFixed(2)+"</td><td>"+parseFloat(file_data[guard_name][0]["net_pay"]).toFixed(2)+"</td><td><a style='cursor:pointer;color:blue' onclick='sendPayslip(\""+guard_name+"\",\""+start_date+"\",\""+end_date+"\")'>Send</a></td></tr>";
	}
	str +="</tbody></table>";
	$("#pay").empty();
	$("#pay").append(str);
}

function DrawTable_eba1(file_data,start_date,end_date,var_state) {
	var file_data = JSON.parse(file_data);
	var str = "<table id='pay_table'><thead><tr><td>Guard Name</td><td>State</td><td>27.00</td><td>27.90</td><td>Leave hours</td><td>Gross Pay</td><td>Tax</td><td>Net Pay</td><td>Payslip</td></tr></thead><tbody>";
	
	for (var i = 0; i < Object.keys(file_data).length; i++) {
			var guard_name = Object.keys(file_data)[i];
			str += "<tr><td>"+guard_name.toUpperCase()+"</td><td>"+var_state+"</td><td>"+file_data[guard_name][0]['day_hours']+"</td><td>"+file_data[guard_name][0]['night_hours']+"</td><td>"+file_data[guard_name][0]["leave_hours"]+"</td><td>"+parseFloat(file_data[guard_name][0]["total_amount"]).toFixed(2)+"</td><td>"+parseFloat(file_data[guard_name][0]["tax"]).toFixed(2)+"</td><td>"+parseFloat(file_data[guard_name][0]["net_pay"]).toFixed(2)+"</td><td><a style='cursor:pointer;color:blue' onclick='sendPayslip(\""+guard_name+"\",\""+start_date+"\",\""+end_date+"\")'>Send</a></td></tr>";
	}
	str +="</tbody></table>";
	$("#pay").empty();
	$("#pay").append(str);
}

function DrawTable_eba2(file_data,start_date,end_date,var_state) {
	var file_data = JSON.parse(file_data);
	var str = "<table id='pay_table'><thead><tr><td>Guard Name</td><td>State</td><td>26.00</td><td>Leave hours</td><td>Gross Pay</td><td>Tax</td><td>Net Pay</td><td>Payslip</td></tr></thead><tbody>";
	
	for (var i = 0; i < Object.keys(file_data).length; i++) {
			var guard_name = Object.keys(file_data)[i];
			str += "<tr><td>"+guard_name.toUpperCase()+"</td><td>"+var_state+"</td><td>"+file_data[guard_name][0]['hours']+"</td><td>"+file_data[guard_name][0]["leave_hours"]+"</td><td>"+parseFloat(file_data[guard_name][0]["total_amount"]).toFixed(2)+"</td><td>"+parseFloat(file_data[guard_name][0]["tax"]).toFixed(2)+"</td><td>"+parseFloat(file_data[guard_name][0]["net_pay"]).toFixed(2)+"</td><td><a style='cursor:pointer;color:blue' onclick='sendPayslip(\""+guard_name+"\",\""+start_date+"\",\""+end_date+"\")'>Send</a></td></tr>";
	}
	str +="</tbody></table>";
	$("#pay").empty();
	$("#pay").append(str);
}

function DrawTable_eba3(file_data,start_date,end_date,var_state) {
	var file_data = JSON.parse(file_data);
	var str = "<table id='pay_table'><thead><tr><td>Guard Name</td><td>State</td><td>26.65</td><td>Leave hours</td><td>Gross Pay</td><td>Tax</td><td>Net Pay</td><td>Payslip</td></tr></thead><tbody>";
	
	for (var i = 0; i < Object.keys(file_data).length; i++) {
			var guard_name = Object.keys(file_data)[i];
			str += "<tr><td>"+guard_name.toUpperCase()+"</td><td>"+var_state+"</td><td>"+file_data[guard_name][0]['hours']+"</td><td>"+file_data[guard_name][0]["leave_hours"]+"</td><td>"+parseFloat(file_data[guard_name][0]["total_amount"]).toFixed(2)+"</td><td>"+parseFloat(file_data[guard_name][0]["tax"]).toFixed(2)+"</td><td>"+parseFloat(file_data[guard_name][0]["net_pay"]).toFixed(2)+"</td><td><a style='cursor:pointer;color:blue' onclick='sendPayslip(\""+guard_name+"\",\""+start_date+"\",\""+end_date+"\")'>Send</a></td></tr>";
	}
	str +="</tbody></table>";
	$("#pay").empty();
	$("#pay").append(str);
}

function DrawTable_awards(file_data,start_date,end_date,category,var_state) {
	var file_data = JSON.parse(file_data);

	if (category == 'security') {
		var str = "<table id='pay_table'><thead><tr><td>Guard Name</td><td>State</td><td>hourly</td><td>saturday</td><td>sunday</td><td>public holiday</td><td>night span</td><td>Leave hours</td><td>Total Amount</td><td>Payslip</td></tr></thead><tbody>";
	
		for (var i = 0; i < Object.keys(file_data).length; i++) {
				var guard_name = Object.keys(file_data)[i];
				str += "<tr><td>"+guard_name.toUpperCase()+"</td><td>"+var_state+"</td><td>"+file_data[guard_name][0]['hourly_hours']+"</td><td>"+file_data[guard_name][0]["saturday_hours"]+"</td><td>"+file_data[guard_name][0]["sunday_hours"]+"</td><td>"+file_data[guard_name][0]["public_holiday_hours"]+"</td><td>"+file_data[guard_name][0]["night_span_hours"]+"</td><td>"+file_data[guard_name][0]["leave_hours"]+"</td><td>"+parseFloat(file_data[guard_name][0]["total_amount"]).toFixed(2)+"</td><td><a style='cursor:pointer;color:blue' onclick='sendPayslip(\""+guard_name+"\",\""+start_date+"\",\""+end_date+"\")'>Send</a></td></tr>";
		}
	}

	if (category == 'cleaning') {
		var str = "<table id='pay_table'><thead><tr><td>Guard Name</td><td>State</td><td>only day hours</td><td>saturday</td><td>sunday</td><td>public holiday</td><td>only night hours</td><td>Day and night hours</td><td>Leave hours</td><td>Total Amount</td><td>Payslip</td></tr></thead><tbody>";
	
		for (var i = 0; i < Object.keys(file_data).length; i++) {
				var guard_name = Object.keys(file_data)[i];
				str += "<tr><td>"+guard_name.toUpperCase()+"</td><td>"+var_state+"</td><td>"+file_data[guard_name][0]['only_day_hours']+"</td><td>"+file_data[guard_name][0]["saturday_hours"]+"</td><td>"+file_data[guard_name][0]["sunday_hours"]+"</td><td>"+file_data[guard_name][0]["public_holiday_hours"]+"</td><td>"+file_data[guard_name][0]["only_night_hours"]+"</td><td>"+file_data[guard_name][0]["day_and_night_hours"]+"</td><td>"+file_data[guard_name][0]["leave_hours"]+"</td><td>"+parseFloat(file_data[guard_name][0]["total_amount"]).toFixed(2)+"</td><td><a style='cursor:pointer;color:blue' onclick='sendPayslip(\""+guard_name+"\",\""+start_date+"\",\""+end_date+"\")'>Send</a></td></tr>";
		}
	}
	
	str +="</tbody></table>";
	$("#pay").empty();
	$("#pay").append(str);
}

function DrawTable_rss(file_data,start_date,end_date,var_state) {
	var file_data = JSON.parse(file_data);
	var str = "<table id='pay_table'><thead><tr><td>Guard Name</td><td>State</td><td>weekday</td><td>weekend</td><td>Leave hours</td><td>Total Amount</td><td>Payslip</td></tr></thead><tbody>";
	
	for (var i = 0; i < Object.keys(file_data).length; i++) {
			var guard_name = Object.keys(file_data)[i];
			str += "<tr><td>"+guard_name.toUpperCase()+"</td><td>"+var_state+"</td><td>"+file_data[guard_name][0]['weekday_hours']+"</td><td>"+file_data[guard_name][0]["weekend_hours"]+"</td><td>"+file_data[guard_name][0]["leave_hours"]+"</td><td>"+parseFloat(file_data[guard_name][0]["total_amount"]).toFixed(2)+"</td><td><a style='cursor:pointer;color:blue' onclick='sendPayslip(\""+guard_name+"\",\""+start_date+"\",\""+end_date+"\")'>Send</a></td></tr>";
	}
	str +="</tbody></table>";
	$("#pay").empty();
	$("#pay").append(str);
}

$(document).ready(function(){
	$('#loading').hide();

	var pay_data = $( "#hidden_pay" ).html();
	var pay_type = $("#pay_type").html();
	var category = $("#category").html();
	var state = $("#state").html();
	var start_date = $( "#hidden_start_date" ).html().replace(/\n/g, '');
	var end_date = $( "#hidden_end_date" ).html().replace(/\n/g, '');
	if(pay_data != '') {
		document.getElementById("download_span").style.display = "block";
		if(pay_type == 'jmd_eba'){
			DrawTable_eba(pay_data,start_date,end_date,state)
		}
		if(pay_type == 'jmd_eba1'){
			DrawTable_eba1(pay_data,start_date,end_date,state)
		}
		if(pay_type == 'jmd_eba2'){
			DrawTable_eba2(pay_data,start_date,end_date,state)
		}
		if(pay_type == 'jmd_eba3'){
			DrawTable_eba3(pay_data,start_date,end_date,state)
		}
		if(pay_type == 'awards'){
			DrawTable_awards(pay_data,start_date,end_date,category,state)
		}
		if(pay_type == 'rss'){
			DrawTable_rss(pay_data,start_date,end_date,state)
		}
	}
})