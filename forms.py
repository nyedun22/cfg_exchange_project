from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField  # BooleanField, DateField, IntegerField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo  # ValidationError


# customer registration form
class CustomerRegistrationForm(FlaskForm):
    # user login elements
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=30), validate_username])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password', message="Passwords must match")])

    # person elements
    first_name = StringField('First Name', validators=[DataRequired(), Length(min=2, max=30)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(min=2, max=30)])
    email = StringField('Email', validators=[DataRequired(), Email(message='Please supply a valid email')])
    # amount =

    # # address elements
    # address_line_one = StringField('Address Line 1', validators=[DataRequired()])
    # address_line_two = StringField('Address Line 2')
    # postcode = StringField('Postcode', validators=[DataRequired()])
    # # submit
    submit = SubmitField('Sign Up')


# customer login form
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email(message='Please supply a valid email')])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')
