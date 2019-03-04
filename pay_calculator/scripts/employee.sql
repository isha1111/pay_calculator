create table employees (
	employee_id serial primary key, 
	firstname varchar(50) NOT NULL, 
	lastname varchar(50),
	date_of_birth varchar(50),
	gender varchar(50),
	mobile int,
	email varchar(50),
	primary_role varchar(50),
	secondary_role varchar(50),
	award_type varchar(50),
	employment_type varchar(50),
	flat_rate int,
	bsb int,
	account int,
	annual_leave float(2),
	sick_leave float(2),
	long_service_leave float(2),
	super float(2),
	notes varchar(10000)
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
	super varchar(50) NOT NULL
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