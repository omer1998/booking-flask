from flask import Flask, request, render_template, send_from_directory, url_for
import auth
app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/preline.js")
def serve_preline_js():
    return send_from_directory("node_modules/preline/dist", "preline.js")

app.register_blueprint(auth.bp)

@app.route("/doctor/appointments")
def appointments():
    return render_template("doctor/appointments.html")
