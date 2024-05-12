import logging
import os
import time
from flask import (
    Blueprint,
    render_template,
    g,
    request,
    redirect,
    url_for,
    flash,
    session
)
from helpers import (login_required)
from db import pool
from psycopg.rows import dict_row
from werkzeug.utils import secure_filename
from datetime import timedelta, datetime

doctor_bp = Blueprint("doctor",__name__, url_prefix="/doctor",static_folder="./static", template_folder="./templates/doctor")

from forms_validation import DoctorUpdateInfoForm
# load doctor; it is a middleware that runs before each request
# the point of this method is to load the doctor from the database and store it in the g object
# so that it can be accessed in the views and also it enable us to check if the doctor is logged in or not in order to restrict certain routes
# login_required is a decorator that checks if the doctor is logged in or not and depend on this function
def generate_doctor_availabilities(doctor_id, days=7 ):
    # this function is used to generate the availabilities of the doctor
    # it is used to generate the availabilities of the doctor for the next 7 days
    try:
        with pool.connection() as conn:
            with conn.cursor(row_factory=dict_row) as cur:
                clinic_info = cur.execute("select * from doctors_clinic where doctor_id = %s", (doctor_id,)).fetchone()
                logging.info(clinic_info)
                patients_num =clinic_info["patient_number_per_day"]
                start_time = clinic_info["start_time"]
                end_time = clinic_info["end_time"]
                holidays = clinic_info["holiday"]
                # construct a datetime from given tima and date in order to make it easier to manipulate the time (adding and substructing)
                start_time = datetime.combine(datetime.today(), start_time)
                end_time = datetime.combine(datetime.today(), end_time)
                working_hours = end_time - start_time
                
                total_working_hours = clinic_info['working_hours']
                appointment_duration_minutes = clinic_info['appointment_duration']
                appointment_duration_minutes = timedelta(minutes=appointment_duration_minutes)
                if patients_num:
                    logging.info("patients number")
                    logging.info(patients_num)
                    duration_per_appoinement = working_hours / patients_num
                    # time_slots_day = generate_time_slots(start_time, end_time, duration_per_appoinement, num_days=days)
                    # time_slots_for_days = generate_slots_for_days(start_time, end_time, duration_per_appoinement, days=days, holidays=holidays)
                    # populate_doctor_availability_table(time_slots_for_days, doctor_id)

                # number_of_slots = int(total_working_hours * 60 / appointment_duration_minutes)
                # time_needed_for_each_patient = timedelta(minutes=appointment_duration_minutes)
                # total_working_hours = timedelta(hours=total_working_hours)
                # num_slots = int(total_working_hours / time_needed_for_each_patient)
                time_slots = generate_slots_for_days(start_time, end_time, appointment_duration_minutes, days=days, holidays=holidays)
                populate_doctor_availability_table(time_slots=time_slots, doctor_id=doctor_id)
                
                # time_slots = [start_time + time_needed_for_each_patient * i for i in range(num_slots)]
                # time_slots = generate_time_slots(start_time, end_time, time_needed_for_each_patient)
                # time_slots_for_3_days = generate_slots_for_days(start_time, end_time, time_needed_for_each_patient, days=3)
                # get the appointments of the doctor for the next 7 days
                # logging.info("time slots for 3 days")
                # logging.info(time_slots_for_3_days)
                # logging.info("first day slots")
                # logging.info(time_slots_for_7_days[0])
                # logging.info("fist slot of first day")
                # # start time of first slot of the first day 
                # logging.info(type(time_slots_for_7_days[0][0][0]))
                # # end time of first slot of the first day
                # logging.info(time_slots_for_7_days[0][0][1])
            
                # number of slots in a day according to the slot period and time needed for each patient
                # number_of_slots = slot_period /timedelta(minutes=15)
                # logging.info(number_of_slots)

                # populate doctor_availability table for doctor_id 6 for one day
                # populate_doctor_availability_table(time_slots_for_3_days, 6)


    except Exception as e:
        logging.info("exception in generate_doctor_availabilities")
        logging.info(str(e))


def generate_time_slots(start_time, end_time, appointment_duration_minutes):
    slots = []
    while start_time < end_time:
        end_slot = start_time + appointment_duration_minutes
        slots.append((start_time, end_slot))
        start_time = end_slot
    return slots

def generate_slots_for_days(start_time, end_time, appointment_duration_minutes ,days= 7, holidays = [6,7]):
    slots = []
    day = start_time.date().strftime("%A") # datetime object --> the day name today
    logging.info(day)
    try:
        for i in range(days):
            if check_holiday(day, holidays):
                start_time = start_time + timedelta(days=1)
                end_time = end_time + timedelta(days=1)
                day = start_time.date().strftime("%A")
                continue
            one_day_slots = generate_time_slots(start_time, end_time, appointment_duration_minutes)
            slots.append(one_day_slots)
            start_time = start_time + timedelta(days=1)
            end_time = end_time + timedelta(days=1)
    except Exception as e:
        logging.info("exception in generate_slots_for_days")
        logging.info(str(e))

    return slots

def get_holidays(holidays=[6,7]):
    holidays_name = []
    for day in holidays:
        if day == 6:
            holidays_name.append("Friday")
        elif day == 7:
            holidays_name.append("Saturday")
        elif day == 1:
            holidays_name.append("Sunday")
        elif day == 2:
            holidays_name.append("Monday")
        elif day == 3:
            holidays_name.append("Tuesday")
        elif day == 4:
            holidays_name.append("Wednesday")
        elif day == 5:
            holidays_name.append("Thursday")
    return holidays_name

def check_holiday(day, holidays=[6,7]):
    if str(day) in get_holidays(holidays):
        return True
    return False
def populate_doctor_availability_table(time_slots, doctor_id):
    # this function is used to populate the doctor_availability table with the availabilities of the doctor
    # the availabilities are the time slots that the doctor is available to receive the patients
    # the time slots are generated by the generate_time_slots function
    # the doctor_id is the id of the doctor
    # date = time_slots[0][0][0].date()
    # logging.info(date)
    days = len(time_slots)
    try:
        with pool.connection() as conn:
            with conn.cursor() as cur:
                for i in range(days):
                    date = time_slots[i][0][0].date()
                    logging.info(date)
                    for slot in time_slots[i]:
                        cur.execute("insert into doctors_availability (start_time, end_time, date, doctor_id) values (%s, %s, %s, %s)", (slot[0], slot[1], date, doctor_id))
    except Exception as e:
        logging.info(str(e))

@doctor_bp.before_app_request
def load_doctor():
    user_id = session.get("user_id")
    if user_id is not None and session["user_type"] == "doctor" and g.get("user") is None:
        try:
            with pool.connection() as conn:
                with conn.cursor(row_factory= dict_row) as cur:
                    doctor = cur.execute("select * from doctors where doctors.id = %s", (session["user_id"],)).fetchone()
                    logging.info(doctor)
                    g.user = doctor
        except Exception as e:
            logging.error(str(e))
            flash(str(e))
            return redirect(url_for("auth.doctor_sign_in"))
    if user_id is None and g.get("user") is not None:
        g.pop("user")
        return redirect(url_for("auth.doctor_sign_in"))
    


# doctor info

@doctor_bp.route("/info", methods= ["GET", "POST"])
@login_required
def doctor_info():
    return render_template("doctor/doctor-update-info.html")
# appointments

@doctor_bp.route("/appointments", methods= ["GET", "POST"])
@login_required
def appointments():
    return render_template("doctor/appointments.html")



@doctor_bp.route("/save-info/<id>", methods= ["GET", "POST"])
def save_info(id):
    logging.info(id)
    form = DoctorUpdateInfoForm()
    if request.method == "POST":
        if form.validate_on_submit():
            first_name = form.first_name.data
            last_name = form.last_name.data
            age = form.age.data
            phone = form.phone.data
            governorate = form.governorate.data
            city = form.city.data
            experience = form.experience.data
            professional_statement = form.professional_statement.data
            specialization = form.specialization.data
           
            
            try:
                with pool.connection() as conn:
                    with conn.cursor() as cur:
                        # check if the post request has the file part
                        if 'file' not in request.files:
                            flash('No file part')
                            return redirect("doctor.save_info", id = id)
                        file = request.files['file']
                        # if user does not select file, browser also
                        # submit an empty part without filename
                        if file.filename == '':
                            flash('No selected file')
                            return redirect("doctor.save_info", id = id)
                        if file:
                            
                            filename = secure_filename(file.filename)
                            file.save(os.path.join(g.get("upload_folder"), filename))
                            cur.execute("insert into doctors_info (first_name, last_name, age, phone, governorate, city, experience, professional_statement, speciality, img_url, doctor_id) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (first_name, last_name, age, str(phone), governorate, city, experience, professional_statement, specialization, filename, id))
                return redirect(url_for("doctor.doctor"))
            except Exception as e:
                flash(str(e))
                return redirect(url_for("doctor.save_info", id = id))
        return render_template("doctor/doctor-info.html", form= form)
    return render_template("doctor/doctor-info.html", form = form, id = id)



@doctor_bp.route("/", methods= ["GET", "POST"])
@login_required
def doctor():
    # this the main proile page (landing page) of the doctor after the doctor sign in
    # retreive the id of this doctor from the session and use it to get the doctor info from the database
    # then render the doctor-landing-page.html with the doctor info
    id = session["user_id"]
    try:
        with pool.connection() as conn:
            with conn.cursor(row_factory=dict_row) as cursor:
                doctor = cursor.execute("select * from doctors_info where doctor_id = %s", (id,)).fetchone()
                logging.info("doctor info")
                logging.info(doctor)
                if not doctor:
                    return redirect(url_for("doctor.save_info"))
                
                # we need to get the appointments of this doctor today
                # we need to get the stats of appointments of this doctor
                # we need to get the questions of the patients of this doctor
                return render_template("doctor-landing-page.html", doctor=doctor)
    except Exception as e:
        flash(str(e))
        return render_template("doctor-landing-page.html")

    

@doctor_bp.route("/doctor-update-info", methods= ["GET", "POST"])
@login_required
def doctor_update_info():
    form = DoctorUpdateInfoForm()
    doctor= None
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            doctor = cur.execute("select * from doctors join doctors_info on doctors.id = doctors_info.doctor_id where doctors.id = %s", (g.user["id"],)).fetchone()       
            
    if request.method == "POST":
        if form.validate_on_submit():
            first_name = form.first_name.data
            last_name = form.last_name.data
            age = form.age.data
            phone = form.phone.data
            governorate = form.governorate.data
            city = form.city.data
            experience = form.experience.data
            professional_statement = form.professional_statement.data
            speciality = form.speciality.data
            try:
                with pool.connection() as conn:
                    with conn.cursor(row_factory=dict_row) as cur:
                        # doctor = cur.execute("select * from doctors join doctors_info on doctors.id = doctors_info.doctor_id where doctors.id = %s", (g.user["id"],)).fetchone()       
                        # cur.execute("update doctors_info set first_name = %s, last_name = %s, age = %s, phone = %s, governorate = %s, city = %s, experience = %s, professional_statement = %s, speciality = %s where id = %s", (first_name, last_name, age, phone, governorate, city, experience, professional_statement, specialization, g.user["id"]))
                        logging.info("updating")
                        # update the doctors_info table or insert if it does not exist
                        cur.execute("""
    INSERT INTO doctors_info (first_name, last_name, age, phone, governorate, city, experience, professional_statement, speciality, doctor_id)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    ON CONFLICT (doctor_id) DO UPDATE
    SET 
    first_name = EXCLUDED.first_name,
    last_name = EXCLUDED.last_name,
    age = EXCLUDED.age,
    phone = EXCLUDED.phone,
    governorate = EXCLUDED.governorate,
    city = EXCLUDED.city,
    experience = EXCLUDED.experience,
    professional_statement = EXCLUDED.professional_statement,
    speciality = EXCLUDED.speciality
    """,
    (first_name, last_name, age, phone, governorate, city, experience, professional_statement, speciality, g.user["id"]))
                return redirect(url_for("doctor.doctor"))
            except Exception as e:
                logging.error(str(e))
                return redirect(url_for("doctor.doctor_update_info"))
        return render_template("doctor/doctor-update-info.html", form= form, doctor = doctor)
    
    else: 
        
        return render_template("doctor/doctor-update-info.html", form= form, doctor = doctor)
                

@doctor_bp.route("/clinic-info", methods= ["GET", "POST"])
@login_required
def clinic_info():
    return render_template("doctor/doctor-clinic.html")                      
                
           
@doctor_bp.route("/doctor_log_out")
@login_required
def doctor_log_out():
    session.clear()
    return redirect(url_for("auth.doctor_sign_in"))

@doctor_bp.route("/patients")
@login_required
def doctor_patients():
    return render_template("doctor/doctor-patients.html")