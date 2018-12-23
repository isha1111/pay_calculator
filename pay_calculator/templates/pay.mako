<%inherit file="layout.mako"/>
<script type="text/javascript" src="/static/js/index.js"></script>
<link rel="stylesheet" type="text/css" href="/static/css/index.css">
<div class="title" id="title">
	<img src="/static/images/jmd_logo.png"></br>
	${project}
</div>
<div class="hidden" id="calculated_data"></div>

<span id="download_span" style="display: none;">
	<img id="download_img" src="/static/images/download_logo.png" onclick="ConvertToCSV()" ></br>
	<span id="download_text" >Download CSV</span>
	
</span>

<div id="hidden_pay" class="hidden"> 
${pay}
</div>

<div id="pay">
	Please wait pay is being calculated ...
</div>
