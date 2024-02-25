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
doctor_bp = Blueprint("doctor",__name__, url_prefix="/doctor",static_folder="./static", template_folder="./templates/doctor")

# load doctor; it is a middleware that runs before each request
# the point of this method is to load the doctor from the database and store it in the g object
# so that it can be accessed in the views and also it enable us to check if the doctor is logged in or not in order to restrict certain routes
# login_required is a decorator that checks if the doctor is logged in or not and depend on this function
@doctor_bp.before_app_request
def load_doctor():
    user_id = session.get("user_id")
    if user_id is not None and session["user_type"] == "doctor" and g.get("user") is None:
        try:
            with pool.connection() as conn:
                with conn.cursor(row_factory= dict_row) as cur:
                    doctor = cur.execute("select * from doctors where id = %s", (session["user_id"],)).fetchone()
                    g.user = doctor
        except Exception as e:
            flash(str(e))
            return redirect(url_for("auth.doctor_sign_in"))


# doctor info

@doctor_bp.route("/info", methods= ["GET", "POST"])
@login_required
def doctor_info():
    return render_template("doctor/doctor-info.html")
# appointments

@doctor_bp.route("/appointments", methods= ["GET", "POST"])
@login_required
def appointments():
    return render_template("doctor/appointments.html")

@doctor_bp.route("/")
@login_required
def doctor():
    return render_template("doctor/doctor-landing-page.html")

@doctor_bp.route("/doctor-update-info")
@login_required
def doctor_update_info():
    return render_template("doctor/doctor-update-info.html", doctor= g.user)

@doctor_bp.route("/doctor_log_out")
@login_required
def doctor_log_out():
    session.clear()
    return redirect(url_for("auth.doctor_sign_in"))

@doctor_bp.route("/patients")
@login_required
def doctor_patients():
    return render_template("doctor/doctor-patients.html")