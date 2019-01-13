<%inherit file="layout.mako"/>
<link rel="stylesheet" type="text/css" href="/static/css/index.css">
<div class="title" id="title">
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
		<label>State</label>
		<select name="state">
			<option value="NSW">NSW</option>
			<option value="VIC">VIC</option>
			<option value="WA">WA</option>
			<option value="ACT">ACT</option>
			<option value="QLD">QLD</option>
			<option value="SA">SA</option>
		</select></br>
		</br>
		<label>Pay Type</label>
		<select>
			<option value="jmd_eba">JMD EBA</option>
			<option value="awards">awards</option>
			<option value="rss">RSS</option>
			<option value="flat_rate">flat rate</option>
		</select></br>
		<label class="label">PLEASE UPLOAD FILE HERE:</label>
		<input type="file" id="roaster_file" accept=".csv" name="roaster_data"></br>
		<input type="submit" id="calculate_input" name="submit" value="CALCULATE PAY" >
	</form>
</div>


