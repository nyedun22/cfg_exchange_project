# still trying to figure out how to link this up, so it runs correctly
# rather than having too much code in app.py file


from flask import render_template
import app, db_utils
from forms import CustomerRegistrationForm, LoginForm

# from db_utils import  # import table names from database


# creating home app route -- example used for now
@app.route('/')
def hello_world():
    return jsonify({'hello':'universe'})


# route for currency convertor
@app.route('/currency')
def currency_convertor():
    return jsonify({'convert': 'currency'})


# route for user sign up form
@app.route('/register')
def user_sign_up():
    return jsonify({'sign': 'up'})


# route for viewing transactions page
@app.route('/transactions')
def transactions():
    return jsonify({'my': 'transactions'})