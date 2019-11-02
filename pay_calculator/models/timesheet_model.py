import psycopg2
from psycopg2 import extras
import json
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# DATABASE_URL = os.environ.get('db_url', None)

DATABASE_URL = 'postgres://lrfdzdjpnximyq:3f1ddb578e598f054626ac0754752cb27d27d14e492aaab2a3b71dcdf50d4265@ec2-54-235-77-0.compute-1.amazonaws.com:5432/dvq1qp8vsr5hr'

def add_timesheet_to_database(shift_date,guard_name,site_name,start_time,end_time,payable_hours):
	conn = psycopg2.connect(DATABASE_URL, sslmode='require')
	cursor = conn.cursor()
	cursor.execute("insert into timesheet(shift_date,guard_name,site_name,start_time,end_time,payable_hours) values (%s,%s,%s,%s,%s,%s)",(shift_date,guard_name,site_name,start_time,end_time,payable_hours))
	conn.commit()
	cursor.close()
	conn.close()