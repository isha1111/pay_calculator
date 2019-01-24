from datetime import date
from dateutil import parser
from datetime import datetime 
from datetime import timedelta

import pandas as pd
import json

from dateutil.relativedelta import relativedelta as rd
from dateutil.relativedelta import MO, TU, WE, TH, FR, SA, SU
import holidays

def calculate_jmd_eba_rate(roaster_data, state):	
	public_day_payrate = 50.53
	weekday_no_rotating_rate = 21
	weekday_rotating_rate = 25

	roaster_data_list = roaster_data.split("\n")
	roaster_row_list = roaster_data_list[1:]

	white_collar_start_time = datetime.strptime('06:00:00', '%H:%M:%S')
	white_collar_end_time = datetime.strptime('18:00:00', '%H:%M:%S')
	day_end_time = datetime.strptime('00:00:00', '%H:%M:%S')
	# day_start_time = datetime.strptime('00:00:00', '%H:%M:%S')

	
	pay = {}
	header = 'Officer full name','Published start date','Published start','Published end','Published actual hours','Published location name','Client name','Officer - Bank Account Name','Officer - BSB','Officer - Bank Account Number'
	
	roaster_dict = {}

	for row in roaster_row_list:
		data = row.split(",")

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
					if guard_shift_day_first in holidays.AU(prov=state):
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
					if guard_shift_day_second in holidays.AU(prov=state):
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

				else:
					first_day_hours = (guard_end_time_object - guard_start_time_object).total_seconds()/3600
					# public holiday
					if guard_shift_day in holidays.AU(prov=state):
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
				total_amount += ((26.68 * total_published_hours) + (20.21 * leave_hours))
			else:
				temp_obj['weekday_and_weeknight_and_weekend_rotating_rate'] = total_published_hours
				temp_obj['weeknight_and_weekend_rotating_rate'] = 0
				total_amount += ((25.12 * total_published_hours) + (20.21 * leave_hours))

		if(public_holiday_hours != 0):
			temp_obj["public_holiday"] = public_holiday_hours
			total_amount += (public_holiday_hours * public_day_payrate)

		temp_obj["total_amount"] = total_amount
		pay[guard_name].append(temp_obj)
    
	return json.dumps(pay)

def calculate_awards_rate(roaster_data, state):

	roaster_data_list = roaster_data.split("\n")
	roaster_row_list = roaster_data_list[1:]

	white_collar_start_time = datetime.strptime('06:00:00', '%H:%M:%S')
	white_collar_end_time = datetime.strptime('18:00:00', '%H:%M:%S')
	day_end_time = datetime.strptime('00:00:00', '%H:%M:%S')
	# day_start_time = datetime.strptime('00:00:00', '%H:%M:%S')

	pay = {}
	header = 'Officer full name','Published start date','Published start','Published end','Published actual hours','Published location name','Client name','Officer - Bank Account Name','Officer - BSB','Officer - Bank Account Number,level'
	
	roaster_dict = {}

	for row in roaster_row_list:
		data = row.split(",")

		guard_name = data[0].lower()
		if guard_name == '':
			continue

		shift_day = data[1]				
		start_time = data[2] 
		end_time = data[3]
		published_hours = data[4]
		level = data[10]

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

			if level == 1:
				hourly_pay_rate = 21.26
				saturday_rate = 31.89
				sunday_rate = 42.52
				public_holiday_rate = 53.15
				mon_fri_night_span_rate = 25.87 

			if level == 2:
				hourly_pay_rate = 21.87
				saturday_rate = 32.81
				sunday_rate = 43.74
				public_holiday_rate = 54.68
				mon_fri_night_span_rate = 26.62

			if level == 3:
				hourly_pay_rate = 22.24
				saturday_rate = 33.36
				sunday_rate = 44.48
				public_holiday_rate = 55.60
				mon_fri_night_span_rate = 27.07

			if level == 4:
				hourly_pay_rate = 22.62
				saturday_rate = 33.93
				sunday_rate = 45.24
				public_holiday_rate = 56.55
				mon_fri_night_span_rate = 27.53

			if level == 5:
				hourly_pay_rate = 23.35
				saturday_rate = 35.03
				sunday_rate = 46.70
				public_holiday_rate = 58.38
				mon_fri_night_span_rate = 28.42
					
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
					if guard_shift_day_first in holidays.AU(prov=state):
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
					if guard_shift_day_second in holidays.AU(prov=state):
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
					if guard_shift_day in holidays.AU(prov=state):
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
		temp_obj['public_holiday_hours'] = round(public_holiday_hours,2)
		temp_obj['night_span_hours'] = round(night_span_hours,2)
		temp_obj['leave_hours'] = leave_hours
		total_pay = (hourly_hours * hourly_pay_rate) + (saturday_hours * saturday_rate) + (sunday_hours * sunday_rate) + (public_holiday_hours * public_holiday_rate) + (night_span_hours * mon_fri_night_span_rate)
		temp_obj["total_amount"] = total_pay
		pay[guard_name].append(temp_obj)
	return json.dumps(pay)

def calculate_rss_rate(roaster_data, state):
	roaster_data_list = roaster_data.split("\n")
	roaster_row_list = roaster_data_list[1:]

	day_end_time = datetime.strptime('00:00:00', '%H:%M:%S')

	pay = {}
	header = 'Officer full name','Published start date','Published start','Published end','Published actual hours','Published location name','Client name','Officer - Bank Account Name','Officer - BSB','Officer - Bank Account Number,level'
	
	roaster_dict = {}

	for row in roaster_row_list:
		data = row.split(",")

		guard_name = data[0].lower()
		if guard_name == '':
			continue

		shift_day = data[1]				
		start_time = data[2] 
		end_time = data[3]
		published_hours = data[4]
		level = data[10]

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

			# check day
			year, month, day = (int(x) for x in guard_shift_day.split('/'))   
			day_number = datetime(year, month, day).weekday()

			# check year
			if year == 2018:
				if level == 1:
					weekday_rate = 21.61
					weekend_rate = 28.41
				if level == 2:
					weekday_rate = 22.23
					weekend_rate = 29.63
				if level == 3:
					weekday_rate = 22.85
					weekend_rate = 30.87
				if level == 4:
					weekday_rate = 23.46
					weekend_rate = 32.11

			if year == 2019:
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
		temp_obj['leave_hours'] = leave_hours
		total_pay = (weekday_rate * weekday_hours) + (weekend_rate * weekend_hours)
		temp_obj['total_amount'] = total_pay
		pay[guard_name].append(temp_obj)
	print(pay)
	return json.dumps(pay)
