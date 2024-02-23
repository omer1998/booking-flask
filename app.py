from flask import Flask, request, render_template, send_from_directory, url_for, session
from flask_session import Session
from datetime import timedelta
import auth
from db import pool
from psycopg.rows import dict_row
app = Flask(__name__)
app.register_blueprint(auth.bp)
# configure the secret key and the session type
app.secret_key= "7a32c13d088e1a704462057aa4e23f464cda8642b7a8cad54b9c0ed263d57ba9"
app.config["SESSION_TYPE"] = "filesystem"
app.config["SESSION_PERMANENT"] = True
# to set the session lifetime to 5 minutes
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(days=3)


Session(app)

@app.route("/") 
def index():
    
    # with pool.connection() as conn:
    #     cursor = conn.cursor(row_factory= dict_row)
    #     result = cursor.execute("select * from doctors").fetchall()
    #     app.logger.info(result)
    # app.logger.info("omer")
    
    return render_template("index.html", session = session)


@app.route("/preline.js")
def serve_preline_js():
    return send_from_directory("node_modules/preline/dist", "preline.js")


@app.route("/doctor/appointments")
def appointments():
    return render_template("doctor/appointments.html")


if __name__ == "__main__":
    app.run(debug=True)