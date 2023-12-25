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
-- psql -U postgres -d booking -a -f schema.sql
-- or -- \i schema_file.sql
-- \d -->  list all table
-- \dt --> list all table that you've created
-- \i --> excute sql from a file