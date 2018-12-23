<%inherit file="layout.mako"/>
<link rel="stylesheet" type="text/css" href="/static/css/index.css">
<div class="title" id="title">
	<img src="/static/images/jmd_logo.png"></br>
	${project}
</div>
<div class="hidden" id="calculated_data"></div>
<div class="form">
	PLEASE UPLOAD FILE TO CALCULATE PAY</br>
	<form enctype="multipart/form-data" action="/calculate_payrate" method="post">
		<input type="file" id="roaster_file" accept=".csv" name="roaster_data">
		<input type="submit" id="calculate_input" name="submit" value="CALCULATE" >
	</form>
</div>


