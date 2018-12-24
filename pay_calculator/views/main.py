from pyramid.view import view_config
from datetime import date
from dateutil import parser
from datetime import datetime 
from datetime import timedelta

import pandas as pd
import json

from dateutil.relativedelta import relativedelta as rd
from dateutil.relativedelta import MO, TU, WE, TH, FR, SA, SU
import holidays

# class VicHolidays(holidays.Australia):
# 	def _populate(self, year):
# 		# get default Australia holidays
# 		holidays.Australia._populate(self, year)
# 		# add grand final day
# 		self[date(year,9,30) + rd(weekday=FR(-1))] = 'Grand Final day Eve'

class NswHolidays(holidays.Australia):
	def _populate(self, year):
		# get default Australia holidays
		holidays.Australia._populate(self, year)
		

@view_config(route_name='home', renderer='../templates/index.mako')
def my_view(request):
    return {'project': 'JMD PAY CALCULATOR','pay':''}

@view_config(route_name='calculate_payrate', renderer='../templates/pay.mako')
def calculate_payrate(request):
	public_day_payrate = 43
	weekday_no_rotating_rate = 21
	weekday_rotating_rate = 25

	white_collar_start_time = datetime.strptime('06:00:00', '%H:%M:%S')
	white_collar_end_time = datetime.strptime('18:00:00', '%H:%M:%S')
	day_end_time = datetime.strptime('00:00:00', '%H:%M:%S')
	# day_start_time = datetime.strptime('00:00:00', '%H:%M:%S')

	roaster_data = request.POST['roaster_data']
	roaster_data = roaster_data.value
	roaster_data = roaster_data.decode('utf-8')

	roaster_data_list = roaster_data.split("\r\n")
	roaster_row_list = roaster_data_list[1:]

	state = request.params.get('state')
	pay = {}
	header = 'Officer full name','Published start date','Published start','Published end','Published actual hours','Published location name','Client name','Officer - Bank Account Name','Officer - BSB','Officer - Bank Account Number'
	

	roaster_dict = {}
	for row in roaster_row_list[1:]:
		data = row.split(",")
		guard_name = data[0].lower()
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

		pay[guard_name] = []
		
		for shift in shifts:
			guard_shift_day = shift['shift_day']
			guard_shift_day = datetime.strptime(guard_shift_day,'%d/%m/%y').strftime('%d/%m/%Y')
			print(guard_shift_day)
			guard_start_time = shift['start_time']
			guard_end_time = shift['end_time']
			published_hours = shift['published_hours']

			# check day
			day, month, year = (int(x) for x in guard_shift_day.split('/'))   
			day_number = datetime(year, month, day).weekday()

			guard_start_time_object = datetime.strptime(guard_start_time, '%H:%M:%S')
			guard_end_time_object = datetime.strptime(guard_end_time, '%H:%M:%S')

			# check if shift is split in two days
			if guard_start_time_object >= guard_end_time_object:
				first_day_hours = (day_end_time - guard_start_time_object).total_seconds()/3600 + 24
				second_day_hours = (guard_end_time_object - day_end_time).total_seconds()/3600
			else:
				first_day_hours = (guard_end_time_object - guard_start_time_object).total_seconds()/3600
				second_day_hours = 0


			if second_day_hours != 0 :
				format_str = '%d/%m/%Y'
				first_day_obj = datetime.strptime(guard_shift_day,format_str).date()
				second_day_obj = datetime.strptime(guard_shift_day,format_str).date() + timedelta(days=1)

				# check for first day
				guard_shift_day_first = guard_shift_day
				guard_shift_day_second = second_day_obj.strftime('%d/%m/%y') #convert to string
				
				# calculate day and night shift time
				night_hours = 0
				day_hours = 0

				# public holiday
				if guard_shift_day_first in NswHolidays(prov=state):
					public_holiday_hours += first_day_hours
				else:
					total_published_hours += published_hours

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
				if guard_shift_day_second in NswHolidays(prov=state):
					public_holiday_hours += second_day_hours
				else:
					# calculate weekday weekend again
					day, month, year = (int(x) for x in guard_shift_day_second.split('/'))   
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
				if guard_shift_day in NswHolidays(prov=state):
					# print(guard_shift_day)
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

		# rule for caluclating if weekday or weeknight payrate
		# print(weeknight_hours)
		# print(weekday_hours)
		# print(weekend_hours)
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
			total_amount += (20.21 * total_published_hours)

		# 2. when no weekday and weekend hours (meaning only weeknight hours in mon-fri outside 06:00 to 18:00)
		if (weekend_hours == 0) and (weekday_hours == 0):
			temp_obj = {}
			temp_obj['weekday_no_rotating_rate'] = 0
			temp_obj['public_holiday_hours'] = public_holiday_hours
			temp_obj['weeknight_no_rotating_rate'] = total_published_hours
			temp_obj['weekday_and_weeknight_rate'] = 0
			temp_obj['weeknight_and_weekend_rotating_rate'] = 0
			temp_obj['weekday_and_weeknight_and_weekend_rotating_rate'] = 0
			total_amount += (24.68 * total_published_hours)

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

			if weeknight_hours > weekday_hours:
				weeknight_hours = weeknight_hours + weekday_hours
				weekday_hours = 0
				temp_obj['weekday_and_weeknight_rate'] = total_published_hours
			else:
				weekday_hours = weekday_hours + weeknight_hours 
				weeknight_hours = 0
				temp_obj['weekday_and_weeknight_rate'] = total_published_hours
			total_amount += (21.11 * total_published_hours)

		# 4. When person works weeknight and weekend and weekday
		if((weekday_hours != 0) and (weeknight_hours != 0) and (weekend_hours != 0)) or (temp_obj is None):
			temp_obj = {}
			total_hours = weeknight_hours + weekend_hours + weekday_hours
			temp_obj['weekday_no_rotating_rate'] = 0
			temp_obj['public_holiday_hours'] = public_holiday_hours
			temp_obj['weeknight_no_rotating_rate'] = 0
			temp_obj['weekday_and_weeknight_rate'] = 0

			if (1/3 * total_hours) > weekday_hours:
				temp_obj['weekday_and_weeknight_and_weekend_rotating_rate'] = 0
				temp_obj['weeknight_and_weekend_rotating_rate'] = total_published_hours
				total_amount += (26.68 * total_published_hours)
			else:
				temp_obj['weekday_and_weeknight_and_weekend_rotating_rate'] = total_published_hours
				temp_obj['weeknight_and_weekend_rotating_rate'] = 0
				total_amount += (25.12 * total_published_hours)

		if(public_holiday_hours != 0):
			temp_obj["public_holiday"] = public_holiday_hours
			total_amount += (public_holiday_hours * public_day_payrate)

		temp_obj["total_amount"] = total_amount
		pay[guard_name].append(temp_obj)
    
	return {'project': 'JMD PAY CALCULATOR','pay':json.dumps(pay)}