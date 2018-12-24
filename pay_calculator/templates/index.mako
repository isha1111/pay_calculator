<%inherit file="layout.mako"/>
<link rel="stylesheet" type="text/css" href="/static/css/index.css">
<div class="title" id="title">
	<img src="/static/images/jmd_logo.png"></br>
	${project}
</div>
<div class="hidden" id="calculated_data"></div>
<div id="instructions" class="center">
	<span class="warning">PLEASE NOTE FOLLOWING:</span></br>
	<div id="instruction-points">
		The <b>excel sheet headers</b> should be same as the one generated from Ento (including header - Officer full name, Published start date, Published start, Published end, Published actual hours, Published location name and so on ...)</br>
	</div>
</div>
<div class="form">
	<form enctype="multipart/form-data" action="/calculate_payrate" method="post">
		<label class="label">PLEASE UPLOAD FILE HERE:</label>
		<input type="file" id="roaster_file" accept=".csv" name="roaster_data"></br>
		<input type="submit" id="calculate_input" name="submit" value="CALCULATE PAY" >
	</form>
</div>


