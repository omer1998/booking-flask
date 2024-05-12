-- create table doctors (
--     id serial primary key,
--     email varchar(20) unique not null,
--     password varchar(20)  not null);

-- create table patients(
--     id serial primary key,
--     email varchar unique not null,
--     password varchar unique not null);

-- create table appointments(
--     id serial primary key,
--     doctor_id int  references doctors(id),
--     patient_id int references patients(id),
--     ap_date date not null,
--     ap_time time not null);

-- create table patients_info(
--     id serial primary key,
--     age int not null,
--     patient_id int references patients(id),
--     disease varchar(20) not null);

-- create table doctors_clinic (
--     address text,
--     latitude text,
--     longitude text,
--     start_time time,
--     end_time time,
--     holiday int[],
--     location geometry(point, 4326),
--     doctor_id int references doctors(id)

-- )
-- psql -U postgres -d booking -a -f schema.sql
-- or -- \i schema_file.sql
-- \d -->  list all table
-- \dt --> list all table that you've created
-- \t table_name --> detail of the table
-- \i --> excute sql from a file

-- delete 
-- DELETE FROM table_name WHERE

-- alter --
-- add column
-- alter table patients add column register_date timestamp with time zone default now();
-- alter table doctors_info 
-- add column province varchar, 
-- add column professional_statement varchar, 
-- add column experience varchar, 
-- add column satisfaction_score integer check (satisfaction_score > 0 and  satisfaction_score <= 10 );

-- alter table patients alter column register_date set not null; 
-- alter table patients alter column register_date drop not null;
-- 
-- ALTER TABLE distributors
--     ALTER COLUMN address TYPE varchar(80),
--     ALTER COLUMN name TYPE varchar(100);

-- to drop a constraint 
-- alter table patients drop constraint patients_password_key;
-- 33.25253065087326, 44.39338199099404

-- INSERT INTO patients_info (patient_id, age, disease, location) values (1, 26, 'priapism', ST_Point(44.39338199099404, 33.25253065087326));

-- we need to create doctors-info table
-- create table doctors_info(
--     id serial primary key,
--     age int not null,
--     doctor_id int references doctors(id) not null,
--     speciality varchar(20) not null,
--     location geometry(point, 4326),
--     city varchar(20) not null,
--     address text not null,
--     phone varchar(20) not null,
--     img_url text 
-- );

-- create table ratings(
-- id serial primary key,
-- patient_id int references patients(id) not null,
-- doctor_id int references doctors(id) not null,
-- rating int not null check (rating > 0 and rating <= 10),
-- review text not null
-- );

-- create table doctors_clinic (
--     id serial primary key,
--     province varchar not null,
--     city varchar not null,
--     address text not null,
--     latitude text not null,
--     longitude text not null,
--     start_time time not null,
--     end_time time not null,
--     working_hours int not null, 
--     holiday int[] not null,
--     location geometry(point, 4326) not null ,
--     price_per_appointment int,
--     patient_number_per_day int,
--     doctor_id int references doctors(id) not null
-- );

-- create function set_working_hours()
-- returns trigger as $$

-- begin
--     new.working_hours := extract(hour from new.end_time) - extract(hour from new.start_time);
--     return new;
-- end;
-- $$ language plpgsql;

-- create function set_location_trigger() 
-- returns trigger as $$
-- begin 
-- new.location := ST_Point(new.longitude::double precision, new.latitude::double precision);
-- return new;
-- end;
-- $$ language plpgsql;

-- create trigger set_location_trigger 
-- before insert on doctors_clinic 
-- for each row 
-- execute function set_location_trigger();

-- create trigger set_working_hours
-- before insert on doctors_clinic
-- for each row
-- execute function set_working_hours();





-- create a trigger function to set the location
-- CREATE OR REPLACE FUNCTION set_location_trigger()
-- RETURNS TRIGGER AS $$
-- BEGIN
--     NEW.location := ST_Point(NEW.latitude::double precision, NEW.longitude::double precision);
--     RETURN NEW;
-- END;
-- $$ LANGUAGE plpgsql;

-- CREATE TRIGGER set_location_trigger
-- BEFORE INSERT ON doctors_clinic
-- FOR EACH ROW
-- EXECUTE FUNCTION set_location_trigger();

-- to drop a trigger
-- drop trigger set_location_trigger on doctors_clinic;

-- to drop a function
-- drop function set_location_trigger();

-- insert into doctors_clinic (province, city, address, latitude, longitude, start_time, end_time, holiday, price_per_appointment, patient_number_per_day, doctor_id) 
-- values 
-- ( 'baghdad', 'al dora', 'al-tuama', '33.25253', '44.39338', '13:00:00', '21:00:00', '{6,7}', 25, 10, 5);


-- questions table

-- create table questions(
--     id serial primary key,
--     question text not null,
--     answer text,
--     doctor_id int references doctors(id) not null,
--     patient_id int references patients(id) not null,
--     created_at timestamp with time zone default now(),
--     answered boolean default false
-- );

-- appointments_details table

-- create table appointments_details(
--     id serial primary key,
--     main_complaint text not null,
--     presnet_illness text not null,
--     past_illness text not null,
--     family_history text not null,
--     drug_history text not null,
--     allergies text not null,
--     doctor_id int references doctors(id) not null,
--     patient_id int references patients(id) not null,
--     appointment_id int references appointments(id) not null

-- );

-- alter table doctors_info add column first_name varchar not null;
-- alter table doctors_info add column last_name varchar not null;

-- alter table patients_info add column first_name varchar not null;
-- alter table patients_info add column last_name varchar not null;
-- alter table patients_info add column past_medical_history text null;
-- alter table patients_info add column family_history text null;
-- alter table patients_info add column drug_history text null;
-- alter table patients_info add column allergies text null;


--drop primary key constraint
-- alter table doctors_clinic drop constraint doctors_clinic_pkey;
-- making id and doctor_id as primary key of doctors_clinic table and prevent any dublicate
-- alter table doctors_clinic add primary key (id );

--  adding unique constraint to doctor_id in doctors_clinic table and doctor_id in doctors_info table in order to prevent any dublicate
-- alter table doctors_clinic add constraint doctor_id unique(doctor_id);
-- alter table doctors_info add constraint doctor unique(doctor_id);

-- adding doctors to db

-- insert into doctors (email, password) values ('ahmedali11@gmail.com', 12345678);
-- insert into doctors_info (age, doctor_id, speciality, city, address, phone, img_url, first_name, last_name) values (30, 6, 'cardiologist', 'baghdad', 'al-tuama', '07777777777', 'https://www.google.com', 'ahmed', 'ali');
-- insert into doctors_clinic (governorate, city, address, latitude, longitude, start_time, end_time, holiday, price_per_appointment, patient_number_per_day, doctor_id) values ('baghdad', 'al dora', 'al-tuama', '33.25253', '44.39338', '13:00:00', '21:00:00', '{6,7}', 25, 10, 6);
-- alter table doctors_clinic rename column province to governorate;

-- insert into doctors_info (age, doctor_id, speciality, governorate, city, phone, img_url, first_name, last_name) values (30, 7, 'urologist', 'baghdad', 'al sader', '07777777777', 'https://www.google.com', 'karar', 'kareem');
-- rename column 
-- alter table doctors_info rename column province to governorate;
-- alter table doctors_info add column governorate varchar not null;
-- alter table doctors_info drop column address;

-- create doctor_avalibility table
-- create table doctors_availability(
--     id serial primary key,
--     doctor_id int references doctors(id) not null,
--     start_time time not null,
--     end_time time not null,
--     date date not null
-- );

-- update doctors_clinic table to include appointment duration in order to calculate the number of patients per day
alter table doctors_clinic add column appointment_duration int not null default 15;