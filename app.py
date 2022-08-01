# run app file to view flask site
from flask import Flask, jsonify, render_template, request, flash
from forms import CustomerRegistrationForm, LoginForm
from currency_codes import get_currencies
from db_setup import mydb, cursor

app = Flask(__name__)
app.config["SECRET_KEY"] = "12345678"


@app.route('/')
def home():
    return render_template('home.html')


# route for currency convertor
@app.route('/currency')
def currency_convertor():
    all_currencies = get_currencies()
    return render_template('currency.html', all_currencies=all_currencies)


# route for user sign up form
@app.route('/register', methods=['GET', 'POST'])
def user_sign_up():
    form = CustomerRegistrationForm()
    # validation for new customer registration form
    if request.method == 'POST':
        username = request.form['username'],
        password = request.form['password'],
        first_name = request.form['first_name'],
        last_name = request.form['last_name'],
        email = request.form['email'],
        address_line_one = request.form['address'],
        postcode = request.form['postcode']

        """if/else statement - if form field input text length less than required user will get error
        otherwise user data will submit to database tables"""
        if len(first_name) == 0 \
                or len(last_name) == 0 \
                or len(email) == 0\
                or len(address_line_one) == 0\
                or len(postcode) == 0\
                or len(password) < 4\
                or len(username) == 0:
            error = "Please complete each section of this form"
        else:
            mydb.user_login = user_sign_up(
                username=username,
                pass_word=password)

            mydb.user_details = user_sign_up(
                first_name=first_name,
                last_name=last_name,
                email=email,
                address=address_line_one,
                postcode=postcode,
                user_login=user_login)

            # cur = mysql.connection.cursor()
            mydb.session.add(user_login)
            mydb.session.add(user_sign_up)
            mydb.session.commit()
            return render_template('home.html', title='Home', form=form)
        return render_template('register.html', title='Register', message=error, form=form)

    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
    else:
        return render_template('register.html', form=form)

    if request.method == 'POST':
        username = request.form['username'],
        password = request.form['password'],
        first_name = request.form['first_name'],
        last_name = request.form['last_name'],
        email = request.form['email'],
        address_line_one = request.form['address'],
        postcode = request.form['postcode']

        """if/else statement - if form field input text length less than required user will get error
        otherwise user data will submit to database tables"""
        if len(first_name) == 0 \
                or len(last_name) == 0 \
                or len(email) == 0\
                or len(address_line_one) == 0\
                or len(postcode) == 0\
                or len(password) < 4\
                or len(username) == 0:
            error = "Please complete each section of this form"
        else:
            print("x")
            mydb.user_login = user_sign_up(username=username, pass_word=pass_word)

            mydb.user_details = user_sign_up(
                first_name=first_name,
                last_name=last_name,
                email=email,
                address_line_one=address_line_one,
                postcode=postcode,
                user_login=user_login)

            # cur = mysql.connection.cursor()
            mydb.session.add(user_login)
            mydb.session.add(user_sign_up)
            mydb.session.commit()
            return render_template('home.html', title='Home', form=form)
        return render_template('register.html', title='Register', message=error, form=form)

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