from flask import (
    Blueprint, render_template, request, session, redirect
)
import logging

from db import pool
from psycopg.rows import dict_row

patient_bp = Blueprint("patient", __name__, url_prefix="/patient", template_folder="templates/patient")

@patient_bp.route("/")
def patient():
    return render_template("main.html")

@patient_bp.route("/make-appointment")
def make_appointment():
    # Get all doctors
    with pool.connection() as con:
        with con.cursor(row_factory=dict_row) as cursor:
            doctors = cursor.execute("select doctor_id, first_name, last_name from doctors_info").fetchall()
            logging.info(doctors)
            return render_template("patient/make-appointment.html", doctors=doctors)
    return render_template("patient/make-appointment.html")

@patient_bp.route("/doctors")
def doctors():
    return render_template("patient/doctors.html")