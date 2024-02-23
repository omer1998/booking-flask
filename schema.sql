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
create table doctors_info(
    id serial primary key,
    age int not null,
    doctor_id int references doctors(id) not null,
    speciality varchar(20) not null,
    location geometry(point, 4326),
    city varchar(20) not null,
    address text not null,
    phone varchar(20) not null,
    img_url text 
);