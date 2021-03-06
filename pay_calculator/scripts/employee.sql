create table employees (
	employee_id serial primary key, 
	firstname varchar(50) NOT NULL, 
	lastname varchar(50),
	date_of_birth varchar(50),
	gender varchar(50),
	mobile varchar(50),
	email varchar(50),
	primary_role varchar(50),
	secondary_role varchar(50),
	award_type varchar(50),
	employment_type varchar(50),
	flat_rate varchar(10),
	bsb varchar(50),
	account varchar(50),
	annual_leave float(2),
	sick_leave float(2),
	long_service_leave float(2),
	super float(2),
	notes varchar(10000),
	security_license varchar(15),
	security_license_expiry varchar(50)
	);

create table site(
	site_id serial primary key,
	sitename varchar(200) NOT NULL,
	notes varchar(500) 
	);

create table timesheet(
	timesheet_id serial primary key,
	shift_date varchar(20) NOT NULL,
	guard_name varchar(50) NOT NULL,
	site_name varchar(50) NOT NULL,
	start_time varchar(10) NOT NULL,
	end_time varchar(10) NOT NULL,
	payable_hours  varchar(10) NOT NULL
	);

create table payslip (
	payslip_id serial primary key, 
	firstname varchar(50) NOT NULL, 
	lastname varchar(50),
	fortnight_start varchar(50) NOT NULL,
	fortnight_end varchar(50) NOT NULL,
	gross_pay varchar(50) NOT NULL,
	net_pay varchar(50) NOT NULL,
	tax varchar(50) NOT NULL,
	super varchar(50) NOT NULL,
	published_hours varchar(100),
	published_rate varchar(100),
	public_holiday_hours varchar(100),
	public_holiday_rate varchar(100),
	weekday_hours varchar(100),
	weekday_rate varchar(100),
	weekend_hours varchar(100),
	weekend_rate varchar(100),
	hourly_hours varchar(100),
	hourly_rate varchar(100),
	saturday_hours varchar(100),
	saturday_rate varchar(100),
	sunday_hours varchar(100),
	sunday_rate varchar(100),
	night_span_hours varchar(100),
	night_span_rate varchar(100)
	);

create table ytd (
	ytd_id serial primary key,
	employee_id int NOT NULL,
	start_year varchar(50) NOT NULL,
	end_year varchar(50) NOT NULL,
	pay varchar(50) NOT NULL,
	tax varchar(50) NOT NULL,
	super_amount varchar(50) NOT NULL
	);

create table users ( 
	user_id serial primary key, 
	username varchar(50) NOT NULL,
	firstname varchar(20) NOT NULL,
	lastname varchar(20) ,
	password varchar(200) NOT NULL,
	role varchar(20),
	creation_date varchar(20) NOT NULL,
	is_admin varchar(20) default FALSE
);