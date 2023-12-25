# let's create authentication blueprint which is an easy way to gather related views

from flask import (
    Blueprint,
    render_template

)

bp = Blueprint("auth",__name__, url_prefix="/auth",static_folder="./static", template_folder="./templates/authentication")

@bp.route("/doctor/sign-up",methods = ["GET", "POST"] )
def doctor_signup():
    return render_template("doctor-sign-up.html")

@bp.route("/doctor/sign-in", methods=["GET", "POST"])
def doctor_sign_in():
    return render_template("doctor-sign-in.html")


@bp.route("/patient/sign-up", methods=["GET", "POST"])
def patient_sign_up():
    return render_template("patient-sign-up.html")

@bp.route("/patient/sign-in", methods=["GET", "POST"])
def patient_sign_in():
    return render_template("patient-sign-in.html")