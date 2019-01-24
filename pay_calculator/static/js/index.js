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
	if(pay_type == 'awards'){
		ConvertToCSV_awards()
	}
	if(pay_type == 'rss'){
		ConvertToCSV_rss()
	}
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
        var header = 'name,20.21,24.68,21.11,26.68,25.12,50.53,leave hours,total_amount\r\n';
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
            line += file_data[guard_name][0]["total_amount"] ;

            str += line + '\r\n';
        }

		var hiddenElement = document.createElement('a');

		hiddenElement.href = 'data:attachment/text,' + encodeURI(str);
		hiddenElement.target = '_blank';
		hiddenElement.download = 'calculated_payrate.csv';
		hiddenElement.click();
    }

function DrawTable_eba(file_data) {
	var file_data = JSON.parse(file_data);
	var str = "<table id='pay_table'><thead><tr><td>Guard Name</td><td>20.21</td><td>24.68</td><td>21.11</td><td>26.68</td><td>25.12</td><td>50.53</td><td>Leave hours</td><td>Total Amount</td></tr></thead><tbody>";
	
	for (var i = 0; i < Object.keys(file_data).length; i++) {
			var guard_name = Object.keys(file_data)[i];
			str += "<tr><td>"+guard_name.toUpperCase()+"</td><td>"+file_data[guard_name][0]['weekday_no_rotating_rate']+"</td><td>"+file_data[guard_name][0]["weeknight_no_rotating_rate"]+"</td><td>"+file_data[guard_name][0]["weekday_and_weeknight_rate"]+"</td><td>"+file_data[guard_name][0]["weeknight_and_weekend_rotating_rate"]+"</td><td>"+file_data[guard_name][0]["weekday_and_weeknight_and_weekend_rotating_rate"]+"</td><td>"+file_data[guard_name][0]["public_holiday_hours"]+"</td><td>"+file_data[guard_name][0]["leave_rate"]+"</td><td>"+parseFloat(file_data[guard_name][0]["total_amount"]).toFixed(2)+"</td></tr>";
	}
	str +="</tbody></table>";
	$("#pay").empty();
	$("#pay").append(str);
}

function DrawTable_awards(file_data) {
	var file_data = JSON.parse(file_data);
	var str = "<table id='pay_table'><thead><tr><td>Guard Name</td><td>hourly</td><td>saturday</td><td>sunday</td><td>public holiday</td><td>night span</td><td>Leave hours</td><td>Total Amount</td></tr></thead><tbody>";
	
	for (var i = 0; i < Object.keys(file_data).length; i++) {
			var guard_name = Object.keys(file_data)[i];
			str += "<tr><td>"+guard_name.toUpperCase()+"</td><td>"+file_data[guard_name][0]['hourly_hours']+"</td><td>"+file_data[guard_name][0]["saturday_hours"]+"</td><td>"+file_data[guard_name][0]["sunday_hours"]+"</td><td>"+file_data[guard_name][0]["public_holiday_hours"]+"</td><td>"+file_data[guard_name][0]["night_span_hours"]+"</td><td>"+file_data[guard_name][0]["leave_hours"]+"</td><td>"+parseFloat(file_data[guard_name][0]["total_amount"]).toFixed(2)+"</td></tr>";
	}
	str +="</tbody></table>";
	$("#pay").empty();
	$("#pay").append(str);
}

function DrawTable_rss(file_data) {
	var file_data = JSON.parse(file_data);
	var str = "<table id='pay_table'><thead><tr><td>Guard Name</td><td>weekday</td><td>weekend</td><td>Leave hours</td><td>Total Amount</td></tr></thead><tbody>";
	
	for (var i = 0; i < Object.keys(file_data).length; i++) {
			var guard_name = Object.keys(file_data)[i];
			str += "<tr><td>"+guard_name.toUpperCase()+"</td><td>"+file_data[guard_name][0]['weekday_hours']+"</td><td>"+file_data[guard_name][0]["weekend_hours"]+"</td><td>"+file_data[guard_name][0]["leave_hours"]+"</td><td>"+parseFloat(file_data[guard_name][0]["total_amount"]).toFixed(2)+"</td></tr>";
	}
	str +="</tbody></table>";
	$("#pay").empty();
	$("#pay").append(str);
}

$(document).ready(function(){
	var pay_data = $( "#hidden_pay" ).html();
	var pay_type = $("#pay_type").html();
	if(pay_data != '') {
		document.getElementById("download_span").style.display = "block";
		if(pay_type == 'jmd_eba'){
			DrawTable_eba(pay_data)
		}
		if(pay_type == 'awards'){
			DrawTable_awards(pay_data)
		}
		if(pay_type == 'rss'){
			DrawTable_rss(pay_data)
		}
	}
})