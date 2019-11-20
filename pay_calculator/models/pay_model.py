from datetime import date
from dateutil import parser
from datetime import datetime 
from datetime import timedelta

import pandas as pd
import json

import math as Math

import holidays
import psycopg2
from psycopg2 import extras

import pdfrw
import os

from urllib.request import urlopen
from urllib.request import Request
from io import StringIO, BytesIO
import PyPDF2 

from pay_calculator.models.holidays import Holidays

# DATABASE_URL = os.environ.get('db_url', None)

DATABASE_URL = 'postgres://lrfdzdjpnximyq:3f1ddb578e598f054626ac0754752cb27d27d14e492aaab2a3b71dcdf50d4265@ec2-54-235-77-0.compute-1.amazonaws.com:5432/dvq1qp8vsr5hr'


### Assumption is made that fortnightly data is being processed ###

def get_ytd_and_pay_data(firstname, start_date,end_date):
	year_start = start_date.split("/")[0]
	year_end = end_date.split("/")[0]
	ytd_year = year_start

	if year_start == year_end:
		if(end_date < ytd_date):
			ytd_year = year_start - 1
	
	conn = psycopg2.connect(DATABASE_URL, sslmode='require')
	cursor = conn.cursor()
	cursor.execute('select * from payslip where firstname = %s and fortnight_start = %s',(firstname,start_date))
	raw_sql =cursor.mogrify('select * from payslip where firstname = %s and fortnight_start = %s',(firstname,start_date))
	pay_data = cursor.fetchall()
	cursor.close()
	conn.close()

	gross_pay = 0
	net_pay = 0
	tax = 0
	super_amount = 0
	published_hours = 0
	public_holiday_hours = 0
	weekday_hours = 0
	weekend_hours = 0
	hourly_hours = 0
	saturday_hours = 0
	sunday_hours = 0
	night_span_hours = 0
	published_rate = 0
	public_holiday_rate = 0
	weekday_rate = 0
	weekend_rate = 0
	hourly_rate = 0
	saturday_rate = 0
	sunday_rate = 0
	night_span_rate = 0

	for row in pay_data:
		firstname = row[1]
		fortnight_start = row[3]
		fortnight_end = row[4]
		gross_pay += round(float(row[5]),2)
		net_pay += round(float(row[6]),2)
		tax += round(float(row[7]),2)
		super_amount += round(float(row[8]),2)
		if row[9] != '':
			published_hours += float(row[9])
			published_rate = float(row[10])
		if row[11] != '':	
			public_holiday_hours += float(row[11])
			public_holiday_rate = float(row[12])
		if row[13] != '':
			weekday_hours += float(row[13])
			weekday_rate = float(row[14])
		if row[15] != '':
			weekend_hours += float(row[15])
			weekend_rate = float(row[16])
		if row[17] != '':
			hourly_hours += float(row[17])
			hourly_rate = float(row[18])
		if row[19] != '':
			saturday_hours += float(row[19])
			saturday_rate = float(row[20])
		if row[21] != '':
			sunday_hours += float(row[21])
			sunday_rate = float(row[22])
		if row[23] != '':
			night_span_hours += float(row[23])
			night_span_rate = float(row[24])

	conn = psycopg2.connect(DATABASE_URL, sslmode='require')
	cursor = conn.cursor()
	cursor.execute('select * from ytd where employee_id = (select employee_id from employees where firstname = %s) and start_year = %s',(firstname,ytd_year))
	ytd_data = cursor.fetchone()
	cursor.close()
	conn.close()
	
	ytd_pay = round(float(ytd_data[4]),2)
	ytd_tax = round(float(ytd_data[5]),2)
	ytd_super_amount = round(float(ytd_data[6]),2)

	return [firstname.title(),fortnight_start,fortnight_end,gross_pay,net_pay,tax,super_amount,ytd_pay,ytd_tax,ytd_super_amount,published_hours,published_rate,public_holiday_hours,public_holiday_rate,weekday_hours,weekday_rate,weekend_hours,weekend_rate,hourly_hours,hourly_rate,saturday_hours,saturday_rate,sunday_hours,sunday_rate,night_span_hours,night_span_rate]

def calculate_jmd_eba_rate(roaster_data, state):	
	public_day_payrate = 50.53
	weekday_rotating_rate = 21.89

	roaster_data_list = roaster_data.split("\n")
	roaster_row_list = roaster_data_list[1:]

	white_collar_start_time = datetime.strptime('06:00:00', '%H:%M:%S')
	white_collar_end_time = datetime.strptime('18:00:00', '%H:%M:%S')
	day_end_time = datetime.strptime('00:00:00', '%H:%M:%S')
	# day_start_time = datetime.strptime('00:00:00', '%H:%M:%S')

	
	pay = {}
	total_dates = []
	header = 'Officer full name','Published start date','Published start','Published end','Published actual hours','Published location name','Client name','Officer - Bank Account Name','Officer - BSB','Officer - Bank Account Number'
	
	roaster_dict = {}

	for row in roaster_row_list:
		data = row.split(",")

		if data[0] == '':
			continue

		if data[1] == '"':
			data.pop(1)

		guard_name = data[0].lower()
		if guard_name == '':
			continue
		shift_day = data[1]				
		start_time = data[2] 
		end_time = data[3]
		published_hours = data[4]

		if guard_name not in roaster_dict:
			roaster_dict[guard_name] = []

		temp_dict = {}
		temp_dict['shift_day'] = shift_day
		temp_dict['start_time'] = start_time
		temp_dict['end_time'] = end_time
		temp_dict['published_hours'] = float(published_hours)

		roaster_dict[guard_name].append(temp_dict)

	for guard_name in roaster_dict:
		shifts = roaster_dict[guard_name]
		num_of_shifts = len(shifts)
		weekday_hours = 0
		weeknight_hours = 0
		weekend_hours = 0
		public_holiday_hours = 0
		total_published_hours = 0
		total_amount = 0
		leave_hours = 0

		pay[guard_name] = []
		
		for shift in shifts:
			guard_shift_day = shift['shift_day']
			type_of_leave = None

			if '-' in guard_shift_day:
				guard_shift_day = datetime.strptime(guard_shift_day,'%Y-%m-%d').strftime('%Y/%m/%d')
			else:
				guard_shift_day = datetime.strptime(guard_shift_day,'%d/%m/%y').strftime('%Y/%m/%d')
			guard_start_time = shift['start_time']
			guard_end_time = shift['end_time']
			published_hours = shift['published_hours']
			total_dates.append(guard_shift_day)

			# check day
			year, month, day = (int(x) for x in guard_shift_day.split('/'))   
			day_number = datetime(year, month, day).weekday()

			if ':' in guard_start_time:
				guard_start_time_object = datetime.strptime(guard_start_time, '%H:%M:%S')
				if guard_end_time == '0:00:00':
					guard_end_time_object = datetime.strptime('23:59:59', '%H:%M:%S')
				else:
					guard_end_time_object = datetime.strptime(guard_end_time, '%H:%M:%S')
			else:
				type_of_leave =  guard_start_time
			# check if shift is split in two days

			if type_of_leave is None:
				if guard_start_time_object > guard_end_time_object:
					first_day_hours = (day_end_time - guard_start_time_object).total_seconds()/3600 + 24
					second_day_hours = (guard_end_time_object - day_end_time).total_seconds()/3600
				else:
					first_day_hours = (guard_end_time_object - guard_start_time_object).total_seconds()/3600
					second_day_hours = 0

				if second_day_hours != 0 :
					format_str = '%Y/%m/%d'
					first_day_obj = datetime.strptime(guard_shift_day,format_str).date()
					second_day_obj = datetime.strptime(guard_shift_day,format_str).date() + timedelta(days=1)

					# check for first day
					guard_shift_day_first = guard_shift_day
					guard_shift_day_second = second_day_obj.strftime('%Y/%m/%d') #convert to string
					# calculate day and night shift time
					night_hours = 0
					day_hours = 0
					temp_total_published_hours = 0
					first_day_pub_holiday = False
					# public holiday
					if datetime.strptime(guard_shift_day_first, '%Y/%m/%d').date() in Holidays.populate(state,year):
						public_holiday_hours += first_day_hours
						first_day_pub_holiday= True							
						temp_total_published_hours = (published_hours - first_day_hours)				
					else:
						temp_total_published_hours = published_hours
						if day_number in [0,1,2,3,4]:
							weekday = True

							# early hours
							if guard_start_time_object < white_collar_start_time:
								temp_night_hours = (white_collar_start_time - guard_start_time_object).total_seconds()/3600
								night_hours += temp_night_hours
							# late hours
							midnight_end_time = datetime.strptime('23:59:59', '%H:%M:%S')
							if guard_start_time_object > white_collar_end_time: #make end time 24
								temp_night_hours = (midnight_end_time - guard_start_time_object).total_seconds()/3600
								night_hours += round(temp_night_hours)
							else:
								night_hours += 6

							if night_hours != 0:
								day_hours = first_day_hours - night_hours
							else:
								day_hours = first_day_hours

							weekday_hours += day_hours
							weeknight_hours += night_hours
						else:
							weekday = False
							weekend_hours += first_day_hours

					# check for second day
					if datetime.strptime(guard_shift_day_second, '%Y/%m/%d').date() in Holidays.populate(state,year):
						if first_day_pub_holiday == False:
							public_holiday_hours += second_day_hours
							temp_total_published_hours = (published_hours - second_day_hours)
						else:
							public_holiday_hours += (published_hours - first_day_hours)
							temp_total_published_hours = 0
					else:
						# calculate weekday weekend again
						year, month, day = (int(x) for x in guard_shift_day_second.split('/'))   
						day_number = datetime(year, month, day).weekday()
						second_night_hours = 0
						if day_number in [0,1,2,3,4]:
							weekday = True

							# early hours
							midnight_start_time = datetime.strptime('00:00:00', '%H:%M:%S')
							if guard_end_time_object < white_collar_start_time: #start time shuld be 0
								temp_night_hours = (guard_end_time_object - midnight_start_time).total_seconds()/3600
								
								second_night_hours += temp_night_hours
								
							else:
								second_night_hours += 6
							# late hours
							if guard_end_time_object > white_collar_end_time: #make end time 24
								temp_night_hours = (guard_end_time_object - white_collar_end_time).total_seconds()/3600
								second_night_hours += temp_night_hours
								
							if second_night_hours != 0:
								day_hours = second_day_hours - second_night_hours
							else:
								day_hours = second_day_hours
							
							weekday_hours += day_hours
							weeknight_hours += second_night_hours

						else:
							weekday = False
							weekend_hours += second_day_hours
					total_published_hours += temp_total_published_hours
				else:
					first_day_hours = (guard_end_time_object - guard_start_time_object).total_seconds()/3600
					# public holiday
					if datetime.strptime(guard_shift_day, '%Y/%m/%d').date() in Holidays.populate(state,year):
						public_holiday_hours += published_hours

					else:
						total_published_hours += published_hours
						if day_number in [0,1,2,3,4]:
							weekday = True				

							# calculate day and night shift time
							night_hours = 0
							day_hours = 0
							
							# early hours
							if guard_start_time_object < white_collar_start_time:
								temp_night_hours = (white_collar_start_time - guard_start_time_object).total_seconds()/3600
								night_hours += temp_night_hours
							# late hours
							if guard_end_time_object > white_collar_end_time: #check for end time 24
								temp_night_hours = (guard_end_time_object - white_collar_end_time).total_seconds()/3600
								night_hours += temp_night_hours


							if night_hours != 0:
								day_hours = first_day_hours - night_hours
							else:
								day_hours = first_day_hours

							weekday_hours += day_hours
							weeknight_hours += night_hours
						else:
							weekday = False
							weekend_hours = first_day_hours
			else:
				leave_hours += published_hours
		# rule for caluclating if weekday or weeknight payrate
		temp_obj = None
		# 1. when no weeknight and weekend hours (meaning that all hours are from mon-fri 06:00 to 18:00)
		if (weeknight_hours == 0) and (weekend_hours == 0):
			temp_obj = {}
			temp_obj['weekday_no_rotating_rate'] = total_published_hours
			temp_obj['public_holiday_hours'] = public_holiday_hours
			temp_obj['weeknight_no_rotating_rate'] = 0
			temp_obj['weekday_and_weeknight_rate'] = 0
			temp_obj['weeknight_and_weekend_rotating_rate'] = 0
			temp_obj['weekday_and_weeknight_and_weekend_rotating_rate'] = 0
			temp_obj['leave_rate'] = leave_hours
			temp_obj['total_published_hours'] = total_published_hours
			temp_obj['total_published_hours_rate'] = 20.21
			total_amount += ((20.21 * total_published_hours) + (20.21 * leave_hours))

		# 2. when no weekday and weekend hours (meaning only weeknight hours in mon-fri outside 06:00 to 18:00)
		if (weekend_hours == 0) and (weekday_hours == 0):
			temp_obj = {}
			temp_obj['weekday_no_rotating_rate'] = 0
			temp_obj['public_holiday_hours'] = public_holiday_hours
			temp_obj['weeknight_no_rotating_rate'] = total_published_hours
			temp_obj['weekday_and_weeknight_rate'] = 0
			temp_obj['weeknight_and_weekend_rotating_rate'] = 0
			temp_obj['weekday_and_weeknight_and_weekend_rotating_rate'] = 0
			temp_obj['leave_rate'] = leave_hours
			temp_obj['total_published_hours'] = total_published_hours
			temp_obj['total_published_hours_rate'] = 24.68
			total_amount += ((24.68 * total_published_hours)+ (20.21 * leave_hours))

		# 3. when person work weeknight and weekday but no weekend
		if(weekend_hours == 0) and (weekday_hours != 0) and (weeknight_hours != 0):
			# check if more than half hours are outside business hours
			temp_obj = {}
			temp_obj['weekday_no_rotating_rate'] = 0
			temp_obj['public_holiday_hours'] = public_holiday_hours
			temp_obj['weeknight_no_rotating_rate'] = 0
			temp_obj['weekday_and_weeknight_rate'] = 0
			temp_obj['weeknight_and_weekend_rotating_rate'] = 0
			temp_obj['weekday_and_weeknight_and_weekend_rotating_rate'] = 0
			temp_obj['leave_rate'] = leave_hours

			if weeknight_hours > weekday_hours:
				weeknight_hours = weeknight_hours + weekday_hours
				weekday_hours = 0
				temp_obj['weekday_and_weeknight_rate'] = total_published_hours
			else:
				weekday_hours = weekday_hours + weeknight_hours 
				weeknight_hours = 0
				temp_obj['weekday_and_weeknight_rate'] = total_published_hours
			temp_obj['total_published_hours'] = total_published_hours
			temp_obj['total_published_hours_rate'] = 21.11
			total_amount += ((21.11 * total_published_hours) + (20.21 * leave_hours))

		# 4. When person works weeknight and weekend and weekday
		if((weekday_hours != 0) and (weeknight_hours != 0) and (weekend_hours != 0)) or (temp_obj is None):
			temp_obj = {}
			total_hours = weeknight_hours + weekend_hours + weekday_hours
			temp_obj['weekday_no_rotating_rate'] = 0
			temp_obj['public_holiday_hours'] = public_holiday_hours
			temp_obj['weeknight_no_rotating_rate'] = 0
			temp_obj['weekday_and_weeknight_rate'] = 0
			temp_obj['leave_rate'] = leave_hours

			if (1/3 * total_hours) > weekday_hours:
				temp_obj['weekday_and_weeknight_and_weekend_rotating_rate'] = 0
				temp_obj['weeknight_and_weekend_rotating_rate'] = total_published_hours
				temp_obj['total_published_hours'] = total_published_hours
				temp_obj['total_published_hours_rate'] = 26.68
				total_amount += ((26.68 * total_published_hours) + (20.21 * leave_hours))
			else:
				temp_obj['weekday_and_weeknight_and_weekend_rotating_rate'] = total_published_hours
				temp_obj['weeknight_and_weekend_rotating_rate'] = 0
				temp_obj['total_published_hours'] = total_published_hours
				temp_obj['total_published_hours_rate'] = 25.12
				total_amount += ((25.12 * total_published_hours) + (20.21 * leave_hours))

		if(public_holiday_hours != 0):
			temp_obj["public_holiday"] = public_holiday_hours
			temp_obj['public_holiday_hours'] = public_holiday_hours
			
			total_amount += (public_holiday_hours * public_day_payrate)
			
		temp_obj['public_holiday_rate'] = public_day_payrate
		temp_obj["total_amount"] = total_amount
		temp_obj["tax"] = calculate_tax(total_amount)
		temp_obj["super"] = calculate_super(total_amount)
		temp_obj["annual_leave"] = calculate_annual_leave(total_published_hours + public_holiday_hours)
		temp_obj["sick_leave"] = calculate_sick_leave(total_published_hours + public_holiday_hours)
		temp_obj["net_pay"] = temp_obj["total_amount"] - temp_obj["tax"]
		temp_obj["guard_shift_day"] = guard_shift_day
		pay[guard_name].append(temp_obj)

	total_dates = list(set(total_dates))
	fortnight_start = min(total_dates)
	fortnight_end = max(total_dates)
    	
	# save_payslip_data(pay,total_dates)
	return [json.dumps(pay),fortnight_start,fortnight_end]

def calculate_tax(pay_amount):
	# calculate for 52 weeks
	num_of_fortnights = 26.07
	yearly_salary = pay_amount * num_of_fortnights

	# calculate tax bracket and deductions
	if yearly_salary <= 18200:
		fortnightly_calculated_tax = 0
	elif (yearly_salary >= 18201) and(yearly_salary <= 37000):
		taxed_salary = yearly_salary - 18200
		yearly_calculated_tax = 0.19 * taxed_salary
		fortnightly_calculated_tax = yearly_calculated_tax / num_of_fortnights
	elif (yearly_salary >= 37001) and(yearly_salary <= 90000):
		fixed_tax = 3572
		taxed_salary = yearly_salary - 37000
		yearly_calculated_tax = (.325 * taxed_salary) + fixed_tax
		fortnightly_calculated_tax = yearly_calculated_tax / num_of_fortnights
	elif (yearly_salary >= 90001) and(yearly_salary <= 	180000):
		fixed_tax = 20797
		taxed_salary = yearly_salary - 90000
		yearly_calculated_tax = (.37 * taxed_salary) + fixed_tax
		fortnightly_calculated_tax = yearly_calculated_tax /num_of_fortnights
	elif (yearly_salary >= 180001):
		fixed_tax = 54097
		taxed_salary = yearly_salary - 180000
		yearly_calculated_tax = (.45 * taxed_salary) + fixed_tax
		fortnightly_calculated_tax = yearly_calculated_tax / num_of_fortnights
	return fortnightly_calculated_tax


def calculate_awards_rate(roaster_data, state, category,job_type):
	print(job_type)
	roaster_data_list = roaster_data.split("\n")
	roaster_row_list = roaster_data_list[1:]

	white_collar_start_time = datetime.strptime('06:00:00', '%H:%M:%S')
	white_collar_end_time = datetime.strptime('18:00:00', '%H:%M:%S')
	day_end_time = datetime.strptime('00:00:00', '%H:%M:%S')
	# day_start_time = datetime.strptime('00:00:00', '%H:%M:%S')

	pay = {}
	total_dates = []
	if job_type == 'part_time':
		header = 'Officer full name','Published start date','Published start','Published end','Published actual hours','Published location name','Client name','Officer - Bank Account Name','Officer - BSB','Officer - Bank Account Number,level,job_type'
	else:
		header = 'Officer full name','Published start date','Published start','Published end','Published actual hours','Published location name','Client name','Officer - Bank Account Name','Officer - BSB','Officer - Bank Account Number,level'
	
	roaster_dict = {}

	for row in roaster_row_list:
		data = row.split(",")

		if data[0] == '':
			continue

		if data[1] == '"':
			data.pop(1)

		guard_name = data[0].lower()
		if guard_name == '':
			continue

		shift_day = data[1]				
		start_time = data[2] 
		end_time = data[3]
		published_hours = data[4]
		level = data[10]

		try:
			job_type = data[11].strip('\r')
		except:
			job_type = ''

		if level not in [1,2,3,4,5]:
			level = 1
		
		if guard_name not in roaster_dict:
			roaster_dict[guard_name] = []

		temp_dict = {}
		temp_dict['shift_day'] = shift_day
		temp_dict['start_time'] = start_time
		temp_dict['end_time'] = end_time
		temp_dict['published_hours'] = float(published_hours)
		temp_dict['level'] = int(level)
		temp_dict['job_type'] = job_type

		roaster_dict[guard_name].append(temp_dict)

	if category == 'security' :
		for guard_name in roaster_dict:
			shifts = roaster_dict[guard_name]
			num_of_shifts = len(shifts)
			hourly_hours = 0
			night_span_hours = 0
			saturday_hours = 0
			sunday_hours = 0
			public_holiday_hours = 0
			total_published_hours = 0
			total_amount = 0
			leave_hours = 0

			pay[guard_name] = []

			for shift in shifts:
				guard_shift_day = shift['shift_day']
				type_of_leave = None

				if '-' in guard_shift_day:
					guard_shift_day = datetime.strptime(guard_shift_day,'%Y-%m-%d').strftime('%Y/%m/%d')
				else:
					guard_shift_day = datetime.strptime(guard_shift_day,'%d/%m/%y').strftime('%Y/%m/%d')

				guard_start_time = shift['start_time']
				guard_end_time = shift['end_time']
				published_hours = shift['published_hours']
				level = shift['level']
				total_dates.append(guard_shift_day)

				if level == 1:
					hourly_pay_rate = 21.90
					saturday_rate = 32.85
					sunday_rate = 43.80
					public_holiday_rate = 54.75
					mon_fri_night_span_rate = 26.65 

				if level == 2:
					hourly_pay_rate = 22.53
					saturday_rate = 33.80
					sunday_rate = 45.06
					public_holiday_rate = 56.33
					mon_fri_night_span_rate = 27.42

				if level == 3:
					hourly_pay_rate = 22.91
					saturday_rate = 34.37
					sunday_rate = 45.82
					public_holiday_rate = 57.28
					mon_fri_night_span_rate = 27.88

				if level == 4:
					hourly_pay_rate = 23.29
					saturday_rate = 34.94
					sunday_rate = 46.58
					public_holiday_rate = 58.23
					mon_fri_night_span_rate = 28.34

				if level == 5:
					hourly_pay_rate = 24.05
					saturday_rate = 36.08
					sunday_rate = 48.10
					public_holiday_rate = 60.13
					mon_fri_night_span_rate = 29.27
						
				# check day
				year, month, day = (int(x) for x in guard_shift_day.split('/'))   
				day_number = datetime(year, month, day).weekday()

				if ':' in guard_start_time:
					guard_start_time_object = datetime.strptime(guard_start_time, '%H:%M:%S')
					if guard_end_time == '0:00:00':
						guard_end_time_object = datetime.strptime('23:59:59', '%H:%M:%S')
					else:
						guard_end_time_object = datetime.strptime(guard_end_time, '%H:%M:%S')

				else:
					type_of_leave =  guard_start_time
				# check if shift is split in two days

				if type_of_leave is None:
					if guard_start_time_object > guard_end_time_object:
						first_day_hours = (day_end_time - guard_start_time_object).total_seconds()/3600 + 24
						second_day_hours = (guard_end_time_object - day_end_time).total_seconds()/3600
					else:
						first_day_hours = (guard_end_time_object - guard_start_time_object).total_seconds()/3600
						second_day_hours = 0

					if second_day_hours != 0 :
						second_day_hours = published_hours - first_day_hours

						format_str = '%Y/%m/%d'
						first_day_obj = datetime.strptime(guard_shift_day,format_str).date()
						second_day_obj = datetime.strptime(guard_shift_day,format_str).date() + timedelta(days=1)
						
						# check for first day
						guard_shift_day_first = guard_shift_day
						guard_shift_day_second = second_day_obj.strftime('%Y/%m/%d') #convert to string
						
						# calculate day and night shift time
						night_hours = 0
						day_hours = 0
						temp_total_published_hours = 0
						first_day_pub_holiday = False
						if datetime.strptime(guard_shift_day_first, '%Y/%m/%d').date() in Holidays.populate(state,year):
							public_holiday_hours += first_day_hours
							first_day_pub_holiday= True							
						else:
							if day_number in [0,1,2,3,4]:
								weekday = True
								# early hours
								if guard_start_time_object < white_collar_start_time:
									temp_night_hours = (white_collar_start_time - guard_start_time_object).total_seconds()/3600
									night_span_hours += temp_night_hours
									night_hours += temp_night_hours
								# late hours
								midnight_end_time = datetime.strptime('23:59:59', '%H:%M:%S')
								if guard_start_time_object > white_collar_end_time: #make end time 24
									temp_night_hours = (midnight_end_time - guard_start_time_object).total_seconds()/3600
									night_span_hours += round(temp_night_hours)
									night_hours += temp_night_hours
								else:
									night_span_hours += 6
									night_hours += 6

								if night_hours != 0:
									hourly_hours += (first_day_hours - night_hours)
								else:
									hourly_hours += first_day_hours
							elif day_number == 5:
								saturday_hours += first_day_hours
							elif day_number == 6:
								sunday_hours += first_day_hours

						# check for second day
						if datetime.strptime(guard_shift_day_second, '%Y/%m/%d').date() in Holidays.populate(state,year):
							if first_day_pub_holiday == False:
								public_holiday_hours += second_day_hours
							else:
								public_holiday_hours += (published_hours - first_day_hours)
						else:
							# calculate weekday weekend again
							year, month, day = (int(x) for x in guard_shift_day_second.split('/'))   
							day_number = datetime(year, month, day).weekday()
							temp_night_hours = 0
							if day_number in [0,1,2,3,4]:
								weekday = True

								# early hours
								midnight_start_time = datetime.strptime('00:00:00', '%H:%M:%S')
								if guard_end_time_object < white_collar_start_time: #start time shuld be 0
									temp_night_hours1 = (guard_end_time_object - midnight_start_time).total_seconds()/3600
									temp_night_hours += temp_night_hours1
									# night_span_hours += temp_night_hours	
								else:
									temp_night_hours += 6

								# late hours
								if guard_end_time_object > white_collar_end_time: #make end time 24
									temp_night_hours1 = (guard_end_time_object - white_collar_end_time).total_seconds()/3600
									temp_night_hours += temp_night_hours1
									# night_span_hours += temp_night_hours
									
								if temp_night_hours != 0:
									if temp_night_hours > second_day_hours:
										night_span_hours += second_day_hours
										hourly_hours += 0
									else:
										night_span_hours += temp_night_hours
										hourly_hours += (second_day_hours - temp_night_hours)
								else:
									hourly_hours += second_day_hours

							elif day_number == 5:
								saturday_hours += second_day_hours
							elif day_number == 6:
								sunday_hours += second_day_hours
					else:
						first_day_hours = (guard_end_time_object - guard_start_time_object).total_seconds()/3600	
						temp_night_hours = 0					
						# public holiday
						if datetime.strptime(guard_shift_day, '%Y/%m/%d').date() in Holidays.populate(state,year):
							public_holiday_hours += published_hours
						else:
							if day_number in [0,1,2,3,4]:
								weekday = True
								# check if there are any outside hours
								if guard_start_time_object < white_collar_start_time:
									temp_night_hours1 = (white_collar_start_time - guard_start_time_object).total_seconds()/3600
									temp_night_hours += temp_night_hours1

								if guard_end_time_object > white_collar_end_time: #check for end time 24
									temp_night_hours1 = (guard_end_time_object - white_collar_end_time).total_seconds()/3600
									temp_night_hours += temp_night_hours1

								if temp_night_hours != 0:
									if temp_night_hours > published_hours:
										hourly_hours += 0
										night_span_hours += published_hours
									else:
										night_span_hours += temp_night_hours
										hourly_hours += published_hours - temp_night_hours
								else:
									hourly_hours += published_hours
									
							elif day_number == 5:
								saturday_hours += published_hours
							elif day_number == 6:
								sunday_hours += published_hours
					
				else:
					leave_hours += published_hours
			# rule for calculating awards pay
			temp_obj = None

			temp_obj = {}
			temp_obj['hourly_hours'] = round(hourly_hours,2) 
			temp_obj['saturday_hours'] = saturday_hours
			temp_obj['sunday_hours'] = sunday_hours
			temp_obj['guard_shift_day'] = guard_shift_day
			temp_obj['public_holiday_hours'] = round(public_holiday_hours,2)
			temp_obj['night_span_hours'] = round(night_span_hours,2)
			temp_obj['hourly_rate'] = hourly_pay_rate
			temp_obj['saturday_rate'] = saturday_rate
			temp_obj['sunday_rate'] = sunday_rate
			temp_obj['public_holiday_rate'] = public_holiday_rate
			temp_obj['night_span_rate'] = mon_fri_night_span_rate
			temp_obj['leave_hours'] = leave_hours
			total_pay = (hourly_hours * hourly_pay_rate) + (saturday_hours * saturday_rate) + (sunday_hours * sunday_rate) + (public_holiday_hours * public_holiday_rate) + (night_span_hours * mon_fri_night_span_rate) + (20.21 * leave_hours)
			total_hours = hourly_hours + saturday_hours + sunday_hours +public_holiday_hours + night_span_hours 
			temp_obj['total_hours'] = total_hours
			temp_obj["total_amount"] = total_pay
			temp_obj["tax"] = calculate_tax(total_pay)
			temp_obj["super"] = calculate_super(total_pay)
			total_worked_hours = hourly_hours + saturday_hours + sunday_hours + public_holiday_hours +night_span_hours
			temp_obj["annual_leave"] = calculate_annual_leave(total_worked_hours)
			temp_obj["sick_leave"] = calculate_sick_leave(total_worked_hours)
			temp_obj["net_pay"] = temp_obj["total_amount"] - temp_obj["tax"]
			pay[guard_name].append(temp_obj)

			total_dates = list(set(total_dates))
			fortnight_start = min(total_dates)
			fortnight_end = max(total_dates)
	
	if category == 'cleaning':
		for guard_name in roaster_dict:
			shifts = roaster_dict[guard_name]
			num_of_shifts = len(shifts)
			only_day_hours = 0
			day_and_night_hours = 0
			only_night_hours = 0
			saturday_hours = 0
			sunday_hours = 0
			public_holiday_hours = 0
			total_published_hours = 0
			total_amount = 0
			leave_hours = 0

			pay[guard_name] = []

			for shift in shifts:
				guard_shift_day = shift['shift_day']
				type_of_leave = None

				if '-' in guard_shift_day:
					guard_shift_day = datetime.strptime(guard_shift_day,'%Y-%m-%d').strftime('%Y/%m/%d')
				else:
					guard_shift_day = datetime.strptime(guard_shift_day,'%d/%m/%y').strftime('%Y/%m/%d')

				guard_start_time = shift['start_time']
				guard_end_time = shift['end_time']
				published_hours = shift['published_hours']
				level = shift['level']
				total_dates.append(guard_shift_day)
				var_job_type = shift['job_type']
				print(var_job_type)
				if var_job_type == 'part_time':
					if level == 1:
						only_day_rate = 23.94
						saturday_rate = 34.35
						sunday_rate = 44.76
						public_holiday_rate = 55.17
						day_and_night_rate = 27.07 
						only_night_rate = 27.07

					if level == 2:
						only_day_rate = 24.77
						saturday_rate = 35.54
						sunday_rate = 46.31
						public_holiday_rate = 57.08
						day_and_night_rate = 28.00
						only_night_rate = 28.00

					if level == 3:
						only_day_rate = 26.11
						saturday_rate = 37.46
						sunday_rate = 48.81
						public_holiday_rate = 56.75
						day_and_night_rate = 29.51
						only_night_rate = 29.51
				else:
					if level == 1:
						only_day_rate = 20.82
						saturday_rate = 31.23
						sunday_rate = 41.64
						public_holiday_rate = 52.05
						day_and_night_rate = 23.94 
						only_night_rate = 27.07

					if level == 2:
						only_day_rate = 21.54
						saturday_rate = 32.31
						sunday_rate = 43.08
						public_holiday_rate = 53.85
						day_and_night_rate = 24.77
						only_night_rate = 28.00

					if level == 3:
						only_day_rate = 22.70
						saturday_rate = 34.05
						sunday_rate = 45.40
						public_holiday_rate = 56.75
						day_and_night_rate = 26.11
						only_night_rate = 29.51
						
				# check day
				year, month, day = (int(x) for x in guard_shift_day.split('/'))   
				day_number = datetime(year, month, day).weekday()

				if ':' in guard_start_time:
					guard_start_time_object = datetime.strptime(guard_start_time, '%H:%M:%S')
					if guard_end_time == '0:00:00':
						guard_end_time_object = datetime.strptime('23:59:59', '%H:%M:%S')
					else:
						guard_end_time_object = datetime.strptime(guard_end_time, '%H:%M:%S')

				else:
					type_of_leave =  guard_start_time
				# check if shift is split in two days

				if type_of_leave is None:
					if guard_start_time_object > guard_end_time_object:
						first_day_hours = (day_end_time - guard_start_time_object).total_seconds()/3600 + 24
						second_day_hours = (guard_end_time_object - day_end_time).total_seconds()/3600
					else:
						first_day_hours = (guard_end_time_object - guard_start_time_object).total_seconds()/3600
						second_day_hours = 0

					if second_day_hours != 0 :
						second_day_hours = published_hours - first_day_hours

						format_str = '%Y/%m/%d'
						first_day_obj = datetime.strptime(guard_shift_day,format_str).date()
						second_day_obj = datetime.strptime(guard_shift_day,format_str).date() + timedelta(days=1)
						
						# check for first day
						guard_shift_day_first = guard_shift_day
						guard_shift_day_second = second_day_obj.strftime('%Y/%m/%d') #convert to string
						
						# calculate day and night shift time
						night_hours = 0
						day_hours = 0
						temp_total_published_hours = 0
						first_day_pub_holiday = False
						if datetime.strptime(guard_shift_day_first, '%Y/%m/%d').date() in Holidays.populate(state,year):
							public_holiday_hours += first_day_hours
							first_day_pub_holiday= True							
						else:
							temp_night_hours = 0
							if day_number == 5:
								saturday_hours += first_day_hours
							elif day_number == 6:
								sunday_hours += first_day_hours
							elif day_number in [0,1,2,3,4]:
								weekday = True
								# early hours
								if guard_start_time_object < white_collar_start_time:
									temp_night_hours += (white_collar_start_time - guard_start_time_object).total_seconds()/3600
								# late hours
								midnight_end_time = datetime.strptime('23:59:59', '%H:%M:%S')
								if guard_start_time_object > white_collar_end_time: #make end time 24
									temp_night_hours += (midnight_end_time - guard_start_time_object).total_seconds()/3600
								else:
									temp_night_hours += 6

								if temp_night_hours != 0:
									if temp_night_hours >= first_day_hours:
										only_night_hours += first_day_hours
									else:
										day_and_night_hours += first_day_hours
								else:
									only_day_hours += first_day_hours

						# check for second day
						if datetime.strptime(guard_shift_day_second, '%Y/%m/%d').date() in Holidays.populate(state,year):
							if first_day_pub_holiday == False:
								public_holiday_hours += second_day_hours
							else:
								public_holiday_hours += (published_hours - first_day_hours)
						else:
							# calculate weekday weekend again
							year, month, day = (int(x) for x in guard_shift_day_second.split('/'))   
							day_number = datetime(year, month, day).weekday()
							temp_night_hours = 0
							if day_number == 5:
								saturday_hours += second_day_hours
							elif day_number == 6:
								sunday_hours += second_day_hours
							elif day_number in [0,1,2,3,4]:
								weekday = True

								# early hours
								midnight_start_time = datetime.strptime('00:00:00', '%H:%M:%S')
								if guard_end_time_object < white_collar_start_time: #start time shuld be 0
									temp_night_hours1 = (guard_end_time_object - midnight_start_time).total_seconds()/3600
									temp_night_hours += temp_night_hours1
									# night_span_hours += temp_night_hours	
								else:
									temp_night_hours += 6

								# late hours
								if guard_end_time_object > white_collar_end_time: #make end time 24
									temp_night_hours1 = (guard_end_time_object - white_collar_end_time).total_seconds()/3600
									temp_night_hours += temp_night_hours1
									# night_span_hours += temp_night_hours
									
								if temp_night_hours != 0:
									if temp_night_hours >= second_day_hours:
										only_night_hours += second_day_hours
									else:
										day_and_night_hours += second_day_hours
								else:
									only_day_hours += second_day_hours
					else:
						first_day_hours = (guard_end_time_object - guard_start_time_object).total_seconds()/3600	
						temp_night_hours = 0
						# public holiday
						if datetime.strptime(guard_shift_day, '%Y/%m/%d').date() in Holidays.populate(state,year):
							public_holiday_hours += published_hours
						else:	
							if day_number == 5:
								saturday_hours += published_hours
							elif day_number == 6:
								sunday_hours += published_hours
							elif day_number in [0,1,2,3,4]:
								weekday = True
								# check if there are any outside hours
								if guard_start_time_object < white_collar_start_time:
									temp_night_hours1 = (white_collar_start_time - guard_start_time_object).total_seconds()/3600
									temp_night_hours += temp_night_hours1

								if guard_end_time_object > white_collar_end_time: #check for end time 24
									temp_night_hours1 = (guard_end_time_object - white_collar_end_time).total_seconds()/3600
									temp_night_hours += temp_night_hours1

								if temp_night_hours != 0:
									if temp_night_hours >= published_hours:
										only_night_hours += published_hours
									else:
										day_and_night_hours += published_hours
								else:
									only_day_hours += published_hours
					
				else:
					leave_hours += published_hours
			# rule for calculating awards pay
			temp_obj = None

			temp_obj = {}
			if (saturday_hours == 0) and (sunday_hours == 0) and (public_holiday_hours == 0):
				if (only_night_hours == 0): 
					if day_and_night_hours != 0:
						day_and_night_hours += only_day_hours
						only_day_hours = 0
				else:
					if day_and_night_hours == 0:
						if only_day_hours != 0:
							day_and_night_hours += only_day_hours
							only_day_hours = 0
							day_and_night_hours += only_night_hours
							only_night_hours = 0
					else:
						day_and_night_hours += only_day_hours
						only_day_hours = 0
						day_and_night_hours += only_night_hours
						only_night_hours = 0
			else:
				if only_night_hours == 0:
					if day_and_night_hours != 0:
						day_and_night_hours += only_day_hours
						only_day_hours = 0
				else:
					day_and_night_hours += only_night_hours
					only_night_hours = 0
					day_and_night_hours += only_day_hours
					only_day_hours = 0

			temp_obj['only_day_hours'] = round(only_day_hours,2) 
			temp_obj['saturday_hours'] = saturday_hours
			temp_obj['sunday_hours'] = sunday_hours
			temp_obj['guard_shift_day'] = guard_shift_day
			temp_obj['public_holiday_hours'] = round(public_holiday_hours,2)
			temp_obj['only_night_hours'] = round(only_night_hours,2)
			temp_obj['day_and_night_hours'] = round(day_and_night_hours,2)
			temp_obj['hourly_rate'] = only_day_rate
			temp_obj['saturday_rate'] = saturday_rate
			temp_obj['sunday_rate'] = sunday_rate
			temp_obj['public_holiday_rate'] = public_holiday_rate
			temp_obj['only_night_rate'] = only_night_rate
			temp_obj['day_and_night_rate'] = day_and_night_rate
			temp_obj['leave_hours'] = leave_hours
			total_pay = (only_day_hours * only_day_rate) + (saturday_hours * saturday_rate) + (sunday_hours * sunday_rate) + (public_holiday_hours * public_holiday_rate) + (only_night_hours * only_night_rate)  + (day_and_night_hours * day_and_night_rate) + (20.82 * leave_hours)

			total_hours = only_day_hours + saturday_hours + sunday_hours +public_holiday_hours + only_night_hours + day_and_night_hours 
			temp_obj['total_hours'] = total_hours
			temp_obj["total_amount"] = total_pay
			temp_obj["tax"] = calculate_tax(total_pay)
			temp_obj["super"] = calculate_super(total_pay)
			total_worked_hours = only_day_hours + saturday_hours + sunday_hours + public_holiday_hours +only_night_hours + day_and_night_hours
			temp_obj["annual_leave"] = calculate_annual_leave(total_worked_hours)
			temp_obj["sick_leave"] = calculate_sick_leave(total_worked_hours)
			temp_obj["net_pay"] = temp_obj["total_amount"] - temp_obj["tax"]
			pay[guard_name].append(temp_obj)

			total_dates = list(set(total_dates))
			fortnight_start = min(total_dates)
			fortnight_end = max(total_dates)

	return [json.dumps(pay), fortnight_start,fortnight_end]

def calculate_rss_rate(roaster_data, state):
	roaster_data_list = roaster_data.split("\n")
	roaster_row_list = roaster_data_list[1:]

	day_end_time = datetime.strptime('00:00:00', '%H:%M:%S')

	pay = {}
	total_dates = []
	header = 'Officer full name','Published start date','Published start','Published end','Published actual hours','Published location name','Client name','Officer - Bank Account Name','Officer - BSB','Officer - Bank Account Number,level'
	
	roaster_dict = {}

	for row in roaster_row_list:
		data = row.split(",")

		if data[0] == '':
			continue

		if data[1] == '"':
			data.pop(1)

		guard_name = data[0].lower()
		if guard_name == '':
			continue

		shift_day = data[1]				
		start_time = data[2] 
		end_time = data[3]
		published_hours = data[4]
		level = data[10]

		if level not in [1,2,3,4,5]:
			level = 1

		if guard_name not in roaster_dict:
			roaster_dict[guard_name] = []

		temp_dict = {}
		temp_dict['shift_day'] = shift_day
		temp_dict['start_time'] = start_time
		temp_dict['end_time'] = end_time
		temp_dict['published_hours'] = float(published_hours)
		temp_dict['level'] = int(level)

		roaster_dict[guard_name].append(temp_dict)

	for guard_name in roaster_dict:
		shifts = roaster_dict[guard_name]
		num_of_shifts = len(shifts)
		weekday_hours = 0
		weekend_hours = 0
		total_published_hours = 0
		total_amount = 0
		leave_hours = 0

		pay[guard_name] = []

		for shift in shifts:
			guard_shift_day = shift['shift_day']
			type_of_leave = None

			if '-' in guard_shift_day:
				guard_shift_day = datetime.strptime(guard_shift_day,'%Y-%m-%d').strftime('%Y/%m/%d')
			else:
				guard_shift_day = datetime.strptime(guard_shift_day,'%d/%m/%y').strftime('%Y/%m/%d')

			guard_start_time = shift['start_time']
			guard_end_time = shift['end_time']
			published_hours = shift['published_hours']
			level = shift['level']
			total_dates.append(guard_shift_day)

			# check day
			year, month, day = (int(x) for x in guard_shift_day.split('/'))   
			day_number = datetime(year, month, day).weekday()

			# check year
			if level == 1:
				weekday_rate = 22.13
				weekend_rate = 29.09
			if level == 2:
				weekday_rate = 22.76
				weekend_rate = 30.34
			if level == 3:
				weekday_rate = 23.40
				weekend_rate = 31.61
			if level == 4:
				weekday_rate = 24.02
				weekend_rate = 32.88

			if ':' in guard_start_time:
				guard_start_time_object = datetime.strptime(guard_start_time, '%H:%M:%S')
				if guard_end_time == '0:00:00':
					guard_end_time_object = datetime.strptime('23:59:59', '%H:%M:%S')
				else:
					guard_end_time_object = datetime.strptime(guard_end_time, '%H:%M:%S')
			else:
				type_of_leave =  guard_start_time

			# check if shift is split into two days
			if type_of_leave is None:
				if guard_start_time_object > guard_end_time_object:
					first_day_hours = (day_end_time - guard_start_time_object).total_seconds()/3600 + 24
					second_day_hours = (guard_end_time_object - day_end_time).total_seconds()/3600
				else:
					first_day_hours = (guard_end_time_object - guard_start_time_object).total_seconds()/3600
					second_day_hours = 0

				if second_day_hours != 0 :
					second_day_hours = published_hours - first_day_hours
					format_str = '%Y/%m/%d'
					first_day_obj = datetime.strptime(guard_shift_day,format_str).date()
					second_day_obj = datetime.strptime(guard_shift_day,format_str).date() + timedelta(days=1)
					
					# check for first day
					guard_shift_day_first = guard_shift_day
					guard_shift_day_second = second_day_obj.strftime('%Y/%m/%d') #convert to string

					if day_number in[0,1,2,3,4]:
						weekday = True
						weekday_hours += first_day_hours
					else:
						weekend_hours += first_day_hours

					# calculate weekday weekend again
					year, month, day = (int(x) for x in guard_shift_day_second.split('/'))   
					day_number = datetime(year, month, day).weekday()

					if day_number in[0,1,2,3,4]:
						weekday = True
						weekday_hours += second_day_hours
					else:
						weekend_hours += second_day_hours
				else:
					if day_number in [0,1,2,3,4]:
						weekday = True
						weekday_hours += published_hours
					else:
						weekday =False
						weekend_hours += published_hours
			else:
				leave_hours += published_hours

		# rule for calculation rss pay
		temp_obj = {}
		temp_obj['weekday_hours'] = round(weekday_hours,2)
		temp_obj['weekend_hours'] = round(weekend_hours,2)
		temp_obj['weekday_rate'] = weekday_rate
		temp_obj['weekend_rate'] = weekend_rate
		temp_obj['leave_hours'] = leave_hours
		temp_obj['guard_shift_day'] = guard_shift_day
		total_pay = (weekday_rate * weekday_hours) + (weekend_rate * weekend_hours) + (20.21 * leave_hours)
		temp_obj['total_amount'] = total_pay
		total_hours = weekend_hours + weekday_hours
		temp_obj['total_hours'] = total_hours
		temp_obj["tax"] = calculate_tax(total_pay)
		total_worked_hours = weekday_hours + weekend_hours
		temp_obj["annual_leave"] = calculate_annual_leave(total_worked_hours)
		temp_obj["sick_leave"] = calculate_sick_leave(total_worked_hours)
		temp_obj["net_pay"] = temp_obj["total_amount"] - temp_obj["tax"]
		temp_obj["super"] = calculate_super(total_pay)
		pay[guard_name].append(temp_obj)

		total_dates = list(set(total_dates))
		fortnight_start = min(total_dates)
		fortnight_end = max(total_dates)
	return [json.dumps(pay),fortnight_start,fortnight_end]

def calculate_jmd_eba3_rate(roaster_data, state):
	roaster_data_list = roaster_data.split("\n")
	roaster_row_list = roaster_data_list[1:]

	day_end_time = datetime.strptime('00:00:00', '%H:%M:%S')

	pay = {}
	total_dates = []
	header = 'Officer full name','Published start date','Published start','Published end','Published actual hours','Published location name','Client name','Officer - Bank Account Name','Officer - BSB','Officer - Bank Account Number,level'
	
	roaster_dict = {}

	for row in roaster_row_list:
		data = row.split(",")

		if data[0] == '':
			continue

		if data[1] == '"':
			data.pop(1)

		guard_name = data[0].lower()
		if guard_name == '':
			continue

		shift_day = data[1]				
		start_time = data[2] 
		end_time = data[3]
		published_hours = data[4]
		level = data[10]

		if level not in [1,2,3,4,5]:
			level = 1

		if guard_name not in roaster_dict:
			roaster_dict[guard_name] = []

		temp_dict = {}
		temp_dict['shift_day'] = shift_day
		temp_dict['start_time'] = start_time
		temp_dict['end_time'] = end_time
		temp_dict['published_hours'] = float(published_hours)
		temp_dict['level'] = int(level)

		roaster_dict[guard_name].append(temp_dict)

	for guard_name in roaster_dict:
		shifts = roaster_dict[guard_name]
		weekday_hours = 0
		total_published_hours = 0
		total_amount = 0
		leave_hours = 0

		pay[guard_name] = []

		for shift in shifts:
			guard_shift_day = shift['shift_day']
			type_of_leave = None

			if '-' in guard_shift_day:
				guard_shift_day = datetime.strptime(guard_shift_day,'%Y-%m-%d').strftime('%Y/%m/%d')
			else:
				guard_shift_day = datetime.strptime(guard_shift_day,'%d/%m/%y').strftime('%Y/%m/%d')

			guard_start_time = shift['start_time']
			guard_end_time = shift['end_time']
			published_hours = shift['published_hours']
			level = shift['level']
			total_dates.append(guard_shift_day)

			# check day
			year, month, day = (int(x) for x in guard_shift_day.split('/'))   
			day_number = datetime(year, month, day).weekday()

			if ':' in guard_start_time:
				guard_start_time_object = datetime.strptime(guard_start_time, '%H:%M:%S')
			else:
				type_of_leave =  guard_start_time

			# check if shift is split into two days
			if type_of_leave is None:
				total_published_hours += published_hours
			else:
				leave_hours += published_hours

		# rule for calculation rss pay
		temp_obj = {}
		temp_obj['hours'] = total_published_hours
		temp_obj['rate'] = 26.65
		temp_obj['leave_hours'] = leave_hours
		total_pay = (26.65 * total_published_hours) + (20.21 * leave_hours)
		temp_obj['total_amount'] = total_pay
		temp_obj["tax"] = calculate_tax(total_pay)
		total_worked_hours = total_published_hours
		temp_obj["annual_leave"] = calculate_annual_leave(total_worked_hours)
		temp_obj["sick_leave"] = calculate_sick_leave(total_worked_hours)
		temp_obj["net_pay"] = temp_obj["total_amount"] - temp_obj["tax"]
		temp_obj["super"] = calculate_super(total_pay)
		pay[guard_name].append(temp_obj)

		total_dates = list(set(total_dates))
		fortnight_start = min(total_dates)
		fortnight_end = max(total_dates)
	return [json.dumps(pay),fortnight_start,fortnight_end]

def calculate_jmd_eba2_rate(roaster_data, state):
	roaster_data_list = roaster_data.split("\n")
	roaster_row_list = roaster_data_list[1:]

	day_end_time = datetime.strptime('00:00:00', '%H:%M:%S')

	pay = {}
	total_dates = []
	header = 'Officer full name','Published start date','Published start','Published end','Published actual hours','Published location name','Client name','Officer - Bank Account Name','Officer - BSB','Officer - Bank Account Number,level'
	
	roaster_dict = {}

	for row in roaster_row_list:
		data = row.split(",")

		if data[0] == '':
			continue

		if data[1] == '"':
			data.pop(1)

		guard_name = data[0].lower()
		if guard_name == '':
			continue

		shift_day = data[1]				
		start_time = data[2] 
		end_time = data[3]
		published_hours = data[4]
		level = data[10]

		if level not in [1,2,3,4,5]:
			level = 1

		if guard_name not in roaster_dict:
			roaster_dict[guard_name] = []

		temp_dict = {}
		temp_dict['shift_day'] = shift_day
		temp_dict['start_time'] = start_time
		temp_dict['end_time'] = end_time
		temp_dict['published_hours'] = float(published_hours)
		temp_dict['level'] = int(level)

		roaster_dict[guard_name].append(temp_dict)

	for guard_name in roaster_dict:
		shifts = roaster_dict[guard_name]
		weekday_hours = 0
		total_published_hours = 0
		total_amount = 0
		leave_hours = 0

		pay[guard_name] = []

		for shift in shifts:
			guard_shift_day = shift['shift_day']
			type_of_leave = None

			if '-' in guard_shift_day:
				guard_shift_day = datetime.strptime(guard_shift_day,'%Y-%m-%d').strftime('%Y/%m/%d')
			else:
				guard_shift_day = datetime.strptime(guard_shift_day,'%d/%m/%y').strftime('%Y/%m/%d')

			guard_start_time = shift['start_time']
			guard_end_time = shift['end_time']
			published_hours = shift['published_hours']
			level = shift['level']
			total_dates.append(guard_shift_day)

			# check day
			year, month, day = (int(x) for x in guard_shift_day.split('/'))   
			day_number = datetime(year, month, day).weekday()

			if ':' in guard_start_time:
				guard_start_time_object = datetime.strptime(guard_start_time, '%H:%M:%S')
			else:
				type_of_leave =  guard_start_time

			# check if shift is split into two days
			if type_of_leave is None:
				total_published_hours += published_hours
			else:
				leave_hours += published_hours

		# rule for calculation rss pay
		temp_obj = {}
		temp_obj['hours'] = total_published_hours
		temp_obj['rate'] = 26.00
		temp_obj['leave_hours'] = leave_hours
		total_pay = (26.00 * total_published_hours) + (20.21 * leave_hours)
		temp_obj['total_amount'] = total_pay
		temp_obj["tax"] = calculate_tax(total_pay)
		total_worked_hours = total_published_hours
		temp_obj["annual_leave"] = calculate_annual_leave(total_worked_hours)
		temp_obj["sick_leave"] = calculate_sick_leave(total_worked_hours)
		temp_obj["net_pay"] = temp_obj["total_amount"] - temp_obj["tax"]
		temp_obj["super"] = calculate_super(total_pay)
		pay[guard_name].append(temp_obj)

		total_dates = list(set(total_dates))
		fortnight_start = min(total_dates)
		fortnight_end = max(total_dates)
	return [json.dumps(pay),fortnight_start,fortnight_end]

def calculate_super(pay_amount):
	super = pay_amount * .095
	return super

def calculate_annual_leave(worked_hours):
	# calculate annual leave for 80 hours
	calculate_leave = .076 * worked_hours	
	return calculate_leave

def calculate_sick_leave(worked_hours):
	# calculate sick leave for 80 hours
	calculate_leave = .038 * worked_hours
	return calculate_leave

def save_leave_data(pay):
	conn = psycopg2.connect(DATABASE_URL, sslmode='require')
	cursor = conn.cursor()

	values_list = []
	new_employees = []
	updated_firstname = []
	rows = []

	all_firstnames = []
	db_firstnames = []
	db_al = []
	db_sl = []

	# first create new employees
	for key in pay:
		first_name = key
		all_firstnames.append(first_name)

	cursor.execute('select firstname, annual_leave,sick_leave from employees where firstname in %(all_firstnames)s ',{'all_firstnames':tuple(all_firstnames)})
	result = cursor.fetchall()

	for row in result:
		db_firstnames.append(row[0])
		db_al.append(row[1])
		db_sl.append(row[2])

	# check what employees not in database
	for key in pay:
		first_name = key
		al = pay[key][0]['annual_leave']
		sl = pay[key][0]['sick_leave']
		if first_name not in db_firstnames:
			values = (first_name,al,sl)
			values_list.append(values)
		else:
			updated_firstname.append(first_name)
			index = db_firstnames.index(first_name)
			annual_leave_calculated = float(db_al[index] + al)
			sick_leave_calculated = float(db_sl[index] + sl)
			temp_obj = {}
			temp_obj["fname"] = first_name
			temp_obj["al"]= annual_leave_calculated
			temp_obj["sl"] = sick_leave_calculated
			rows.append(temp_obj)

	if len(values_list) != 0:	
		extras.execute_values(cursor,"insert into employees (firstname,annual_leave,sick_leave) values %s", values_list)
		conn.commit()

	if len(updated_firstname) != 0:
		# now check for remainder employees
		cursor.executemany("update employees set annual_leave = %(al)s, sick_leave = %(sl)s where firstname = %(fname)s",tuple(rows))
		conn.commit()

	cursor.close()
	conn.close()

def save_payslip_data(pay,fortnight_start,fortnight_end):

	firstname_list = []	
	
	conn = psycopg2.connect(DATABASE_URL, sslmode='require')
	cursor = conn.cursor()

	values_list = []
	for key in pay:
		first_name = key
		firstname_list.append(first_name)
		gross_pay = pay[key][0]['total_amount']
		net_pay = pay[key][0]['net_pay']
		super_amount = pay[key][0]['super']
		tax = pay[key][0]['tax']

		if 'total_published_hours' in pay[key][0]:
			total_published_hours = pay[key][0]['total_published_hours']
			total_published_hours_rate = pay[key][0]['total_published_hours_rate']
		else:
			total_published_hours = ''
			total_published_hours_rate = ''

		if 'public_holiday_hours' in pay[key][0]:
			total_public_holiday_hours = pay[key][0]['public_holiday_hours']
			total_public_holiday_hours_rate = pay[key][0]['public_holiday_rate']
		else:
			total_public_holiday_hours = ''
			total_public_holiday_hours_rate = ''

		if 'weekday_hours' in pay[key][0]:
			weekday_hours = pay[key][0]['weekday_hours']
			weekday_rate = pay[key][0]['weekday_rate']
		else:
			weekday_hours = ''
			weekday_rate = ''

		if 'weekend_hours' in pay[key][0]:
			weekend_hours = pay[key][0]['weekend_hours']
			weekend_rate = pay[key][0]['weekend_rate']
		else:
			weekend_hours = ''
			weekend_rate = ''

		if 'hourly_hours' in pay[key][0]:
			hourly_hours = pay[key][0]['hourly_hours']
			hourly_rate = pay[key][0]['hourly_rate']
		else:
			hourly_hours = ''
			hourly_rate = ''

		if 'saturday_hours' in pay[key][0]:
			saturday_hours = pay[key][0]['saturday_hours']
			saturday_rate = pay[key][0]['saturday_rate']
		else:
			saturday_hours = ''
			saturday_rate = ''

		if 'sunday_hours' in pay[key][0]:
			sunday_hours = pay[key][0]['sunday_hours']
			sunday_rate = pay[key][0]['sunday_rate']
		else:
			sunday_hours = ''
			sunday_rate = ''

		if 'night_span_hours' in pay[key][0]:
			night_span_hours = pay[key][0]['night_span_hours']
			night_span_rate = pay[key][0]['night_span_rate']
		else:
			night_span_hours = ''
			night_span_rate = ''

		values = (first_name,'',fortnight_start,fortnight_end,gross_pay,net_pay,tax,super_amount,total_published_hours,total_published_hours_rate,total_public_holiday_hours,total_public_holiday_hours_rate,weekday_hours,weekday_rate,weekend_hours,weekend_rate,hourly_hours,hourly_rate,saturday_hours,saturday_rate,sunday_hours,sunday_rate,night_span_hours,night_span_rate)
		values_list.append(values)
	extras.execute_values(cursor,"insert into payslip (firstname, lastname, fortnight_start, fortnight_end, gross_pay, net_pay, tax, super,published_hours,published_rate,public_holiday_hours,public_holiday_rate,weekday_hours,weekday_rate,weekend_hours,weekend_rate,hourly_hours,hourly_rate,saturday_hours,saturday_rate,sunday_hours,sunday_rate,night_span_hours,night_span_rate) VALUES %s", values_list)
	conn.commit()

	# update ytd and create ytd if not there
	# check if ytd row exist for employee and year
	year_start = fortnight_start.split("/")[0]
	year_end = fortnight_end.split("/")[0]
	year_start1 = ''
	values_list_ytd = []
	values_list_ytd1 = []
	values_list_ytd2 = []
	rows = []

	if year_start == year_end:
		ytd_date = '30/6/'+year_end
		# 1. when start date > 30 Jun
		if(fortnight_end >= ytd_date):
			year_end = year_end + 1
		# 2. when end date < 30 Jun
		else:
			year_start = year_start - 1


	if year_start1 == '':
		# get the exsiting ytd data
		cursor.execute("select ytd.ytd_id,ytd.pay,ytd.tax,ytd.super_amount, employees.firstname from ytd left join employees on ytd.employee_id = employees.employee_id where employees.firstname in %s and ytd.start_year = %s", (tuple(firstname_list),year_start))
		result = cursor.fetchall()

		db_ytd_id = []
		db_pay = []
		db_tax = []
		db_super = []
		db_firstname =[]
		not_db_firstname = []

		for row in result:
			db_ytd_id.append(row[0])
			db_pay.append(float(row[1]))
			db_tax.append(float(row[2]))
			db_super.append(float(row[3]))
			db_firstname.append(row[4])

		for key in pay:
			fname = key
			if fname not in db_firstname:
				not_db_firstname.append(fname)

		employee_to_id = {}

		if len(not_db_firstname) != 0:		
			cursor.execute("select employee_id,firstname from employees where firstname in %s",(tuple(not_db_firstname),))
			result = cursor.fetchall()

			for row in result:
				employee_to_id[row[1]]=row[0]

		for key in pay:
			first_name = key
			gross_pay = pay[key][0]['total_amount']/2
			net_pay = pay[key][0]['net_pay']/2
			super_amount = pay[key][0]['super']/2
			tax = pay[key][0]['tax']/2

		# if not present create ytd data
			if first_name not in db_firstname:
				e_id = employee_to_id[first_name]
				values = (e_id,year_start,year_end,gross_pay,tax,super_amount)
				values_list_ytd.append(values)
			else:
				temp_obj = {}
				index = db_firstname.index(first_name)
				temp_obj["ytd_id"] = db_ytd_id[index]
				temp_obj["year_start"] = year_start
				temp_obj["year_end"]= year_end
				temp_obj["gross_pay"] = float(db_pay[index] + gross_pay)
				temp_obj["tax"] = float(db_tax[index] + tax)
				temp_obj["super_amount"] = float(db_super[index] + super_amount)
				rows.append(temp_obj)

		# create
		if len(values_list_ytd) != 0:	
			extras.execute_values(cursor,"insert into ytd (employee_id,start_year,end_year,pay,tax,super_amount) values %s", values_list_ytd)
			conn.commit()

		# update
		if len(rows) != 0:
			cursor.executemany("update ytd set pay = %(gross_pay)s, tax = %(tax)s, super_amount = %(super_amount)s where ytd_id = %(ytd_id)s", tuple(rows))
			conn.commit()

	cursor.close()
	conn.close()


	
def write_fillable_pdf(input_pdf_path, output_pdf_path, data_dict):
	ANNOT_KEY = '/Annots'
	ANNOT_FIELD_KEY = '/T'
	ANNOT_VAL_KEY = '/V'
	ANNOT_RECT_KEY = '/Rect'
	SUBTYPE_KEY = '/Subtype'
	WIDGET_SUBTYPE_KEY = '/Widget'

	template_pdf = pdfrw.PdfReader(input_pdf_path)
	annotations = template_pdf.pages[0][ANNOT_KEY]
	
	for annotation in annotations:
		if annotation[SUBTYPE_KEY] == WIDGET_SUBTYPE_KEY:
			if annotation[ANNOT_FIELD_KEY]:
				key = annotation[ANNOT_FIELD_KEY][1:-1]
				if key in data_dict.keys():
  					annotation.update(pdfrw.PdfDict(V='{}'.format(data_dict[key])))

	pdfrw.PdfWriter().write(output_pdf_path, template_pdf)

