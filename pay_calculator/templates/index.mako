<%inherit file="layout.mako"/>
<script type="text/javascript" src="/static/js/index.js"></script>
<link rel="stylesheet" type="text/css" href="/static/css/index.css">
<div class="title" id="title">
	<img src="/static/images/jmd_logo.png"></br>
	${project}
</div>
<div class="hidden" id="calculated_data"></div>
<div class="form">
	PLEASE UPLOAD FILE TO CALCULATE PAY</br>
	<input type="file" id="roaster_file" accept=".csv" >
	<button id="calculate_button" onclick="csv_reader()">Calculate</button>
</div>
<!-- Select city:
<select id="state">
	<option value="NSW">NSW</option>
	<option value="VIC">VIC</option>
</select> -->
<span id="download_span" style="display: none;">
	<img id="download_img" src="/static/images/download_logo.png" onclick="ConvertToCSV()" ></br>
	<span id="download_text" >Download CSV</span>
	
</span>
<div id="pay">
	
</div>
