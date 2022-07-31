# run app file to view flask site
from flask import Flask, jsonify, render_template, request
from forms import CustomerRegistrationForm, LoginForm
from currency_codes import get_currencies

app = Flask(__name__)
app.config["SECRET_KEY"] = "12345678"


@app.route('/')
def home():
    return render_template('home.html')


# route for currency convertor
@app.route('/currency')
def currency_convertor():
    all_currencies = get_currencies()
    return render_template('currency.html', all_currencies = all_currencies)


# route for user sign up form
@app.route('/register')
def user_sign_up():
    form = CustomerRegistrationForm()
    return render_template('register.html', form=form)

# route for user login form
@app.route('/login')
def user_login():
    form = LoginForm()
    return render_template('login.html', form=form)

# route for viewing transactions pagefl
@app.route('/transactions')
def transactions():
    return render_template('transactions.html')


if __name__ == '__main__':
    # app.run(debug=True, host='0.0.0.0')
    app.run(debug=True, port=5003)