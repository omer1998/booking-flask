from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField, IntegerField, DateField, SelectField, TimeField
from wtforms.validators import DataRequired, Email, EqualTo, Length, InputRequired

class DoctorSignUpForm(FlaskForm):
    email = EmailField("email", validators=[DataRequired(), Email()])
    password = PasswordField("password", validators=[DataRequired(), Length(min=8)])
    password_confirm = PasswordField("password_confirm", validators=[DataRequired(), EqualTo("password")])

class DoctorSignInForm(FlaskForm):
    email = EmailField("email", validators=[DataRequired(), Email()])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8)])

class PatientSignUpForm(FlaskForm):
    email = EmailField("email", validators=[DataRequired(), Email()])
    password = PasswordField("password", validators=[DataRequired(), Length(min=8)])
    password_confirm = PasswordField("password_confirm", validators=[DataRequired(), EqualTo("password")])


class PatientSignInForm(FlaskForm):
    email = EmailField("email", validators=[DataRequired(), Email()])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8)])

class DoctorUpdateInfoForm(FlaskForm):
    first_name = StringField("first_name", validators=[DataRequired()])
    last_name = StringField("last_name", validators=[DataRequired()])
    age = IntegerField("age", validators=[DataRequired()])
    phone = StringField("phone", validators=[DataRequired()])
    governorate = StringField("governorate", validators=[DataRequired()])
    city = StringField("city", validators=[DataRequired()])
    experience = StringField("experience",)
    professional_statement = StringField("professional_statement", )
    speciality = StringField("speciality", validators=[DataRequired()])
    

class MakeAppointmentForm(FlaskForm):
    doctor_id = IntegerField("doctor_id", validators=[DataRequired()])
    date = DateField("date", validators=[DataRequired()])
    time = TimeField("time", validators=[DataRequired()])