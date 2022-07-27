import mysql.connector
from config import *
from mysql.connector import Error

mydb = mysql.connector.connect(
    host= HOST,
    user= USER,
    passwd= PASSWORD,
)

create_db_cursor = mydb.cursor()

create_db_cursor.execute(f"CREATE DATABASE {DATABASE_NAME}")
create_db_cursor.close()

try:
    connection = mysql.connector.connect(host= HOST,
                                         database= DATABASE_NAME,
                                         user= USER,
                                         password= PASSWORD)
    if connection.is_connected():
        cursor = connection.cursor()
        cursor.execute("CREATE TABLE user_details(user_ID INTEGER(10) NOT NULL AUTO_INCREMENT, first_name VARCHAR(255) NOT NULL, last_name VARCHAR(255) NOT NULL, username VARCHAR(255) NOT NULL, pass_word CHAR(10) NOT NULL, PRIMARY KEY (user_ID))")
        cursor.execute("CREATE TABLE bank_details (account_number INTEGER(8) NOT NULL UNIQUE, user_ID INTEGER(10) NOT NULL AUTO_INCREMENT, sort_code CHAR(8) NOT NULL, currency CHAR(3) NOT NULL, main_account_balance NUMERIC(20,2), PRIMARY KEY (account_number), FOREIGN KEY (user_ID) REFERENCES user_details(user_ID))")
        cursor.execute("CREATE TABLE foreign_account(foreign_account_number INTEGER(8) NOT NULL UNIQUE, account_number INTEGER(8) NOT NULL UNIQUE, foreign_account_balance NUMERIC(20,2) NOT NULL, foreign_currency CHAR(3) NOT NULL, PRIMARY KEY (foreign_account_number), FOREIGN KEY (account_number) REFERENCES bank_details(account_number))")
        cursor.execute("CREATE TABLE transactions(transaction_ID INTEGER(20) NOT NULL UNIQUE, account_number INTEGER(8) NOT NULL UNIQUE, foreign_account_number INTEGER(8) NOT NULL UNIQUE, date DATETIME NOT NULL, foreign_currency CHAR (3) NOT NULL, gbp_amount NUMERIC(20,2), foreign_currency_amount NUMERIC(20,2), exchange_rate NUMERIC(10,6), PRIMARY KEY (transaction_ID), FOREIGN KEY (account_number) REFERENCES bank_details(account_number), FOREIGN KEY (foreign_account_number) REFERENCES foreign_account(foreign_account_number))")

except Error as e:
    print("Error while connecting to MySQL", e)
finally:
    if connection.is_connected():
        cursor.close()
        connection.close()
        
## PERFORMING FUNCTIONS ON THE DATABASE ##

class Bank_User:

    def __init__(self):
        self.username = None
        self.password = None
        self.user_id = None
        self.cur_account_number = None
        self.cur_bank_balance = 0
        self.for_bank_balance = 0

    #function to get username
    def get_username(self, username_input):
        db_connection = _connect_to_db()
        mycursor = db_connection.cursor()
        username_query = ('SELECT IF (EXISTS(SELECT username FROM user_details WHERE username = %s), 1, 0)')
        mycursor.execute(username_query, (username_input, ))
        for x in mycursor:
            self.username = x[0] #username stored as 1 (if exists) or 0 (if not exists)

    #function to get password
    def get_password(self, username_input):
        db_connection = _connect_to_db()
        mycursor = db_connection.cursor()
        query = ('SELECT pass_word FROM user_details WHERE username = %s')
        mycursor.execute(query, (username_input,))
        for x in mycursor:
            self.password = x[0]

    #function to get the user_id
    def get_user_id(self, username_input, password_input):
        db_connection = _connect_to_db()
        mycursor = db_connection.cursor()
        user_id_return = ('SELECT user_id FROM user_details WHERE username = %s AND pass_word = %s')
        mycursor.execute(user_id_return, (username_input, password_input))
        for x in mycursor:
            user_id = x[0]
            self.user_id = user_id

    # function which verifies username and password and if they are a match it will return user id:
    def login_verification(self): #can also pass username and password through as arguement, maybe change to this when front end has been set up
        username_input = input('username:')  # simulates user input
        try:
            self.get_username(username_input)
            if self.username == 0:
                raise Exception
        except:
            print('Username not recognised')
        else:
            password_input = input('password:')  # simulates user input
            self.get_password(username_input)
            if self.password == password_input:
                print('Login Successful')
                self.get_user_id(username_input, password_input)
            else:
                print('Incorrect Password')


    #function to check current account balance and update class with bank balance and bank ID
    def balance_check(self): #again might change this to pass through user_amount as argument
        db_connection = _connect_to_db()
        mycursor = db_connection.cursor()
        query = ('SELECT main_account_balance, account_number FROM bank_details b JOIN user_details u ON u.user_id = b.user_id WHERE u.user_id = %s')
        mycursor.execute(query, (self.user_id, ))
        for x in mycursor:
            bank_balance = x[0]
            account_number = x[1]
            self.cur_bank_balance = bank_balance
            self.cur_account_number = account_number

    #function which creates a new account
    #using dummy exchange rate, this will be passed through as param later
    def create_foreign_account(self, user_amount):
        DUMXCH = 2
        db_connection = _connect_to_db()
        mycursor = db_connection.cursor()
        query = ('INSERT INTO foreign_account (account_number, foreign_account_balance, foreign_currency) VALUES (%s, %s, %s)')
        foreign_money = user_amount * DUMXCH
        self.for_bank_balance += foreign_money
        mycursor.execute(query, (self.cur_account_number, self.for_bank_balance, 'DUMXCH'))
        db_connection.commit()

    #function which updates current account bank balance
    def update_current_account(self, user_amount):
        db_connection = _connect_to_db()
        mycursor = db_connection.cursor()
        query = ('UPDATE bank_details SET main_account_balance = (%s) WHERE account_number = (%s)')
        self.cur_bank_balance = self.cur_bank_balance - user_amount
        mycursor.execute(query, (self.cur_bank_balance, self.cur_account_number))
        db_connection.commit()

    #function to record transaction

    #function to print current account balance

    #function to provide details of new foreign exchange account

    #function to create new current account

    #transaction which moves money from one account to another -using other functions within the function
    def xchange_transaction(self):
        db_connection = _connect_to_db()
        mycursor = db_connection.cursor()
        try:
            self.balance_check()
            user_amount = input('How much do you want to exchange in GBP?')
            user_amount = int(user_amount)
            if user_amount > self.cur_bank_balance:
                raise Exception
        except:
            print('Insufficient funds for this transaction, please try again')
        else:
            #need to offer conversion rate, for now dummy exchange rate
            #user then needs to accept conversion rate
            #update current account balance
            self.update_current_account(user_amount)
            #create and update foreign currency account
            self.create_foreign_account(user_amount)
            print('You have successfully transferred £{} into {} {}'.format(user_amount, user_amount*2, 'DUMXCH'))
            print('New Current Account Balance: {} GBP'.format(self.cur_bank_balance))
            print('New Foreign Currency Account Balance: {} {}'.format(self.for_bank_balance, 'DUMXCH'))
        finally:
            db_connection.close()

    #function to reset class
    def reset_user(self):
        self.username = None
        self.password = None
        self.user_id = None
        self.cur_account_number = None
        self.cur_bank_balance = 0
        self.for_bank_balance = 0



user = Bank_User()

user.login_verification()
#print('After Login\n'
#      'Username:{}\nPassword:{}\nUserID:{}\nBankID:{}\nBankBalance:{}\nForeignCurrency:{}'.format(user.username, user.password, user.user_id, user.bank_id, user.bank_balance, user.foreign_currency))
user.xchange_transaction()
#print('After Transaction \n'
#      'Username:{}\nPassword:{}\nUserID:{}\nBankID:{}\nBankBalance:{}\nForeignCurrency:{}'.format(user.username, user.password, user.user_id, user.bank_id, user.bank_balance, user.foreign_currency))
user.reset_user()
