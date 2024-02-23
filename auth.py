# let's create authentication blueprint which is an easy way to gather related views
from werkzeug.security import generate_password_hash, check_password_hash

from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    session

)
import logging
from db import pool
from forms_validation import (DoctorSignUpForm, DoctorSignInForm )
from psycopg.rows import dict_row # this is a row factory that returns a dictionary instead of a tuple for each row in the result set of each executed query

bp = Blueprint("auth",__name__, url_prefix="/auth",static_folder="./static", template_folder="./templates/authentication")

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
                    with conn.cursor() as cur:
                        doctor = cur.execute("select * from doctors where email = %s", (email,)).fetchone()
                        if doctor:
                            flash("You've already registered !!")
                            return redirect(url_for('auth.doctor_sign_up'))
                        password_hash = generate_password_hash(password=password)
                        cur.execute("insert into doctors (email, password) values (%s, %s)", (email, password_hash))
                        return redirect(url_for("auth.doctor_sign_in"))
                    
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
                return redirect(url_for("index"))
    
    return render_template("doctor-sign-in.html", form= form )


@bp.route("/patient/sign-up", methods=["GET", "POST"])
def patient_sign_up():
    return render_template("patient-sign-up.html")

@bp.route("/patient/sign-in", methods=["GET", "POST"])
def patient_sign_in():
    return render_template("patient-sign-in.html")