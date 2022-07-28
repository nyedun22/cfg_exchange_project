from flask import Flask, jsonify, render_template
from forms import CustomerRegistrationForm
from flask_wtf.csrf import CSRFProtect, CSRFError

# run app file to view flask site
app = Flask(__name__)
csrf = CSRFProtect(app)
app.config["SECRET_KEY"] = "12345678"


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
    form = CustomerRegistrationForm()
    return render_template('register.html', form=form)


# route for viewing transactions page
@app.route('/transactions')
def transactions():
    return jsonify({'my': 'transactions'})


if __name__ == '__main__':
    # app.run(debug=True, host='0.0.0.0')
    app.run(debug=True, port=5003)
