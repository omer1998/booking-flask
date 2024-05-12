# let's create authentication blueprint which is an easy way to gather related views
from werkzeug.security import generate_password_hash, check_password_hash

from flask import (
    Blueprint,
    g,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    session

)
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
from doctor import generate_doctor_availabilities

import pytz
import logging
from db import pool
from forms_validation import (DoctorSignUpForm, DoctorSignInForm, PatientSignUpForm, PatientSignInForm )
from psycopg.rows import dict_row # this is a row factory that returns a dictionary instead of a tuple for each row in the result set of each executed query

bp = Blueprint("auth",__name__, url_prefix="/auth",static_folder="./static", template_folder="./templates/authentication")

# configure schedualing process
scheduler = BackgroundScheduler()
scheduler.start()
@bp.route("/doctor/sign-up",methods = ["GET", "POST"] )
def doctor_sign_up():
    form = DoctorSignUpForm(request.form)
    # get email and password from the form
    # check if the email is already in the database
    # if it is, return an error message
    # if it is not, insert the email and password into the database
    # return redirect(url_for("auth.doctor_sign_in"))
    # email = request.form["email"]
    # password = request.form["password"]
    if request.method == "POST":
   
        if form.validate_on_submit():
            email = form.email.data
            password = form.password.data
            # password_confirm = form.password_confirm.data
            
            try:
                with pool.connection() as conn:
                    with conn.cursor(row_factory=dict_row) as cur:
                        doctor = cur.execute("select * from doctors where email = %s", (email,)).fetchone()
                        if doctor:
                            flash("You've already registered !!")
                            return redirect(url_for('auth.doctor_sign_up'))
                        password_hash = generate_password_hash(password=password)
                        cur.execute("insert into doctors (email, password) values (%s, %s)", (email, password_hash))
                        doctor = cur.execute("select * from doctors where email = %s", (email,)).fetchone()
                        # hashing the id of the doctor
                        
                        return redirect(url_for("doctor.save_info", id = doctor["id"]))
                    
            except Exception as e:
                print(e)
                flash(str(e))
                return redirect(url_for("auth.doctor_sign_up"))
        
    
    if request.method == "GET":
        return render_template("doctor-sign-up.html", form = form)


         
    # return render_template("doctor-sign-up.html")

@bp.route("/doctor/sign-in", methods=["GET", "POST"])
def doctor_sign_in():
    form = DoctorSignInForm()
    email = form.email.data
    password = form.password.data
    if request.method == "POST":
        with pool.connection() as conn:
            with conn.cursor(row_factory= dict_row) as cur:
                doctor = cur.execute("select * from doctors where email = %s", (email,)).fetchone()
                logging.info(doctor)
                if doctor is None:
                    flash("No such user")
                    return redirect(url_for("auth.doctor_sign_in"))
                if not check_password_hash(doctor["password"], password):
                    flash("Incorrect password")
                    return redirect(url_for("auth.doctor_sign_in"))
                # if the email and password are correct, set the session variables
                session['user_type'] = 'doctor'
                session['user_id'] = doctor['id']
                g.user = doctor
                # check if the job of populating the availabilities is already running or available
                job = scheduler.get_job(f'populating_availabilities_job_{doctor["id"]}')
                logging.info('job')
                logging.info(job)

                time_now = datetime.now(pytz.timezone("Asia/Baghdad"))
                logging.info("time_now")
                logging.info(doctor["id"])
                # def print_hello():
                #     print("hello world, this is cs50 final project")
                if not job or job.next_run_time <= time_now:
                    if job:
                        scheduler.remove_job(f'populating_availabilities_job_{doctor["id"]}')
                    # scheduler.add_job(generate_doctor_availabilities, args=[6, 1], 
                    #                   id=f'populating_availabilities_job_{doctor["id"]}', 
                    #                   trigger="interval",
                    #                   minutes=1,
                    #                   next_run_time=time_now
                    #                   )
                    
                    # scheduler.print_jobs()
                return redirect(url_for("doctor.doctor"))
                return redirect(url_for("index"))
    
    return render_template("doctor-sign-in.html", form= form )


@bp.route("/patient/sign-up", methods=["GET", "POST"])
def patient_sign_up():
    form = PatientSignUpForm()

    if request.method == "POST":
        password = form.password.data
        password_confirm = form.password_confirm.data
        logging.info(password)
        logging.info(password_confirm)  

        if password != password_confirm:
            flash("Passwords don't match")
            logging.info("Passwords don't match")
            return redirect(url_for("auth.patient_sign_up"))
        if form.validate_on_submit():
            email = form.email.data
            password = form.password.data
            password_confirm = form.password_confirm.data
            if password != password_confirm:
                flash("Passwords don't match")
                logging.info("Passwords don't match")
                return redirect(url_for("auth.patient_sign_up"))
            try:
                with pool.connection() as conn:
                    with conn.cursor() as cur:
                        patient = cur.execute("select * from patients where email = %s", (email,)).fetchone()
                        if patient:
                            flash("You've already registered")
                            return redirect(url_for("auth.patient_sign_up"))
                        password_hash = generate_password_hash(password)
                        cur.execute("insert into patients (email, password) values (%s, %s)", (email, password_hash))
                        return redirect(url_for("auth.patient_sign_in"))
            except Exception as e:
                flash(str(e))
                return redirect(url_for("auth.patient_sign_up"))
        # logging.info(request.form["email"])
        return render_template("./patient-sign-up.html", form = form)

    return render_template("./patient-sign-up.html", form = form)

@bp.route("/patient/sign-in", methods=["GET", "POST"])
def patient_sign_in():
    form = PatientSignInForm()
    if request.method == "POST":
        if form.validate_on_submit():
            email = form.email.data
            password = form.password.data
            logging.info(email)
            logging.info(password)
            try:
                with pool.connection() as conn:
                    with conn.cursor(row_factory=dict_row) as cur:
                        patient = cur.execute("select * from patients where email = %s ", (email,)).fetchone()
                        if patient is None :
                            flash("No such user")
                            return redirect(url_for("auth.patient_sign_in"))
                        if not check_password_hash(patient["password"], password):
                            flash("Incorrect password")
                            return redirect(url_for("auth.patient_sign_in"))
                        if patient["email"] == email and check_password_hash(patient["password"], password):
                            session["user_type"] = "patient"
                            session["user_id"] = patient["id"]
                            return redirect(url_for("patient.patient"))
            except Exception as e:
                flash(str(e))
                return redirect(url_for("auth.patient_sign_in"))
        return render_template("patient-sign-in.html", form = form)
    return render_template("patient-sign-in.html", form = form)