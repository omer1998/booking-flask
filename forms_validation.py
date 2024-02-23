from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField
from wtforms.validators import DataRequired, Email, EqualTo, Length, InputRequired

class DoctorSignUpForm(FlaskForm):
    email = EmailField("email", validators=[DataRequired(), Email()])
    password = PasswordField("password", validators=[DataRequired(), Length(min=8)])
    password_confirm = PasswordField("password_confirm", validators=[DataRequired(), EqualTo("password")])

class DoctorSignInForm(FlaskForm):
    email = EmailField("email", validators=[DataRequired(), Email()])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8)])