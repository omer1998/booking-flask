import logging
from flask import Flask, g, request, render_template, send_from_directory, url_for, session
from flask_session import Session
from datetime import timedelta
import auth
from db import pool
from psycopg.rows import dict_row
from doctor import doctor_bp, generate_doctor_availabilities
from patient import patient_bp

app = Flask(__name__)
app.register_blueprint(auth.bp)
app.register_blueprint(doctor_bp)
app.register_blueprint(patient_bp)

# configure the secret key and the session type
app.secret_key= "7a32c13d088e1a704462057aa4e23f464cda8642b7a8cad54b9c0ed263d57ba9"
app.config["SESSION_TYPE"] = "filesystem"
app.config["SESSION_PERMANENT"] = True
# to set the session lifetime to 5 minutes
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(minutes=30)

# set up uploading
UPLOAD_FOLDER = "./uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
with app.app_context():
    g.upload_folder = UPLOAD_FOLDER



Session(app)

@app.route("/") 
def index():
    
    # with pool.connection() as conn:
    #     cursor = conn.cursor(row_factory= dict_row)
    #     result = cursor.execute("select * from doctors").fetchall()
    #     app.logger.info(result)
    # app.logger.info("omer")
    
    return render_template("index.html", session = session)

# @app.route("/doctor") 
# def doctor():
    
    
#     return render_template("doctor/doctor-landing-page.html")


@app.route("/preline.js")
def serve_preline_js():
    return send_from_directory("node_modules/preline/dist", "preline.js")


@app.route("/doctor/appointments")
def appointments():
    return render_template("doctor/appointments.html")


if __name__ == "__main__":
    generate_doctor_availabilities(doctor_id=6 , days=1)
    app.run(debug=True)