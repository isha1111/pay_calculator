<%inherit file="../layout.mako"/>
<script type="text/javascript" src="/static/js/index.js"></script>
<link rel="stylesheet" type="text/css" href="/static/css/index.css">
<div class="title" id="title">
	${project}
</div>
<div class="hidden" id="content">
	<span id="pay_type">${pay_type}</span>
</div>
<div class="hidden" id="calculated_data"></div>
<a id="index_tag" href="/" class="center">Calculate another pay</a>
<span id="download_span" style="display: none;">
	<img id="download_img" src="/static/images/download_logo.png" onclick="download_data()" ></br>
	<span id="download_text" >Download CSV</span>
	
</span>

<div id="hidden_pay" class="hidden"> 
${pay}
</div>

<div id="pay">
	Please wait pay is being calculated ...
</div>
