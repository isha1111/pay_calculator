<%inherit file="../layout.mako"/>
<link rel="stylesheet" type="text/css" href="/static/css/employee/payslip.css">

<div id="container">
	<div id="form_div">
		<div id="paid_by">
			PAID BY:

		</div>
		<div id="emp_details">
			EMPLOYMENT DETAILS <br>
			Pay Frequencey: Fortnightly<br>
			Annual Salary: Something
		</div>
		<div>

			<div>
				${payslip_data[0]} <br>
				Address: 121212 <br>
				765858 087879
			</div>
			<br>
		</div>
		<div>
			<hr>
			<div class="inline"><b>Pay Period</b>: ${payslip_data[1]}- ${payslip_data[2]}</div>
			<div class="inline"><b>Payment Date</b>: todays date</div>
			<div class="inline"><b>Total Earning</b>: ${payslip_data[3]}</div>
			<div class="inline"><b>Net Pay</b>: ${payslip_data[4]}</div>
			<hr>
			<br>
			<table>
				<tr>
					<td></td>
					<td></td>
					<td></td>
					<td></td>
					<td><b>This Pay</b></td>
					<td><b>YTD</b></td>
				</tr>
				<tr>
					<td>SALARY & WAGES</td>
					<td></td>
					<td>PAY RATE</td>
					<td>HOURS</td>
					<td></td>
					<td></td>
				</tr>
				% if payslip_data[10] != '':
				<tr>
					<td>Ordinary Hours</td>
					<td></td>
					<td>${payslip_data[11]}</td>
					<td>${payslip_data[10]}</td>
					<td>
					<% 
						total= float(payslip_data[10]) * float(payslip_data[11])
						total = round(total,2)
					%> ${total}</td>
					<td></td>
				</tr>
				% endif
				% if payslip_data[12] != '':
				<tr>
					<td>Public Holiday Hours</td>
					<td></td>
					<td>${payslip_data[13]}</td>
					<td>${payslip_data[12]}</td>
					<td>
					<% 
						total= float(payslip_data[13]) * float(payslip_data[12])
						total = round(total,2)
					%> ${total}</td>
					<td></td>
				</tr>
				% endif
				% if payslip_data[14] != '':
				<tr>
					<td>Weekday Hours</td>
					<td></td>
					<td>${payslip_data[15]}</td>
					<td>${payslip_data[14]}</td>
					<td>
					<% 
						total= float(payslip_data[15]) * float(payslip_data[14])
						total = round(total,2)
					%> ${total}</td>
					<td></td>
				</tr>
				% endif
				% if payslip_data[17] != '':
				<tr>
					<td>Weekday Hours</td>
					<td></td>
					<td>${payslip_data[17]}</td>
					<td>${payslip_data[16]}</td>
					<td>
					<% 
						total= float(payslip_data[17]) * float(payslip_data[16])
						total = round(total,2)
					%> ${total}</td>
					<td></td>
				</tr>
				% endif
				% if payslip_data[19] != '':
				<tr>
					<td>Normal Hours</td>
					<td></td>
					<td>${payslip_data[19]}</td>
					<td>${payslip_data[18]}</td>
					<td>
					<% 
						total= float(payslip_data[19]) * float(payslip_data[18])
						total = round(total,2)
					%> ${total}</td>
					<td></td>
				</tr>
				% endif
				% if payslip_data[21] != '':
				<tr>
					<td>Saturday Hours</td>
					<td></td>
					<td>${payslip_data[21]}</td>
					<td>${payslip_data[20]}</td>
					<td>
					<% 
						total= float(payslip_data[21]) * float(payslip_data[20])
						total = round(total,2)
					%> ${total}</td>
					<td></td>
				</tr>
				% endif
				% if payslip_data[23] != '':
				<tr>
					<td>Sunday Hours</td>
					<td></td>
					<td>${payslip_data[23]}</td>
					<td>${payslip_data[22]}</td>
					<td>
					<% 
						total= float(payslip_data[23]) * float(payslip_data[22])
						total = round(total,2)
					%> ${total}</td>
					<td></td>
				</tr>
				% endif
				% if payslip_data[25] != '':
				<tr>
					<td>Night Hours</td>
					<td></td>
					<td>${payslip_data[25]}</td>
					<td>${payslip_data[24]}</td>
					<td>
					<% 
						total= float(payslip_data[25]) * float(payslip_data[24])
						total = round(total,2)
					%> ${total}</td>
					<td></td>
				</tr>
				% endif
				<tr class="gray">
					<td></td>
					<td></td>
					<td></td>
					<td>TOTAL</td>
					<td><b>${payslip_data[3]}</b></td>
					<td><b>${payslip_data[7]}</b></td>
				</tr>
				<tr>
					<td></td>
					<td></td>
					<td></td>
					<td></td>
					<td></td>
					<td></td>
				</tr>
				<tr>
					<td>TAX</td>
					<td></td>
					<td></td>
					<td></td>
					<td></td>
					<td></td>
				</tr>
				<tr>
					<td>PAYG TAX</td>
					<td></td>
					<td></td>
					<td></td>
					<td>${payslip_data[5]}</td>
					<td>${payslip_data[8]}</td>
				</tr>
				<tr class="gray">
					<td></td>
					<td></td>
					<td></td>
					<td>TOTAL</td>
					<td><b>${payslip_data[5]}</b></td>
					<td><b>${payslip_data[8]}</b></td>
				</tr>
				<tr>
					<td></td>
					<td></td>
					<td></td>
					<td></td>
					<td></td>
					<td></td>
				</tr>
				<tr>
					<td>SUPERANNUATION</td>
					<td></td>
					<td></td>
					<td></td>
					<td></td>
					<td></td>
				</tr>
				<tr>
					<td>SUPER FUNDS</td>
					<td></td>
					<td></td>
					<td></td>
					<td>${payslip_data[6]}</td>
					<td>${payslip_data[9]}</td>
				</tr>
				<tr class="gray">
					<td></td>
					<td></td>
					<td></td>
					<td>TOTAL</td>
					<td><b>${payslip_data[6]}</b></td>
					<td><b>${payslip_data[9]}</b></td>
				</tr>
				<tr>
					
				</tr>
				<tr>
					<td>PAYMENT DETAILS</td>
					<td></td>
					<td></td>
					<td></td>
					<td>REFERENCE</td>
					<td>AMOUNT</td>
				</tr>
				<tr>
					<td>${payslip_data[0]}</td>
					<td></td>
					<td></td>
					<td></td>
					<td>WAGES</td>
					<td>${payslip_data[4]}</td>
				</tr>
			</table>
			<br>

		</div>
		
	</div>
</div>