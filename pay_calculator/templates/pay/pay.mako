<%inherit file="../layout.mako"/>
<script type="text/javascript" src="/static/js/index.js"></script>
<link rel="stylesheet" type="text/css" href="/static/css/index.css">
<div class="title" id="title">
	${project}
</div>
<div class="hidden" id="content">
	<span id="pay_type">${pay_type}</span>
	<span id="category">${category}</span>
</div>
<div class="hidden" id="calculated_data"></div>
<a id="index_tag" href="/" class="center">Calculate another pay</a>
<span id="download_span" style="display: none;">
	<img id="download_img" src="/static/images/download_logo.png" onclick="download_data()" ></br>
	<span id="download_text" >Download CSV</span>
	
</span>
<span id="leave_button" href="/" class="center" onclick="generate_and_save_leave()">Generate Leave</span>
<span id="payslip_button" href="/" class="center" onclick="generate_and_save_payslip()">Generate payslip</span>

<div id="hidden_pay" class="hidden"> 
${pay}
</div>

<div id="hidden_start_date" class="hidden"> 
${fortnight_start}
</div>

<div id="hidden_end_date" class="hidden"> 
${fortnight_end}
</div>

<div id="pay">
	Please wait pay is being calculated ...
</div>

<div id="loading">
	<div id="loading_msg">Please wait ...</div>	
  <img id="loading-image" src="/static/images/loading.svg" alt="Loading..." />
</div>
