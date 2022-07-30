import mysql.connector
from config import *
from mysql.connector import Error

def _connect_to_db():
    db_connection = mysql.connector.connect(
        host=HOST,
        user=USER,
        password=PASSWORD,
        database=DATABASE_NAME
    )
    return db_connection
        
## PERFORMING FUNCTIONS ON THE DATABASE ##

class Bank_User:

    def __init__(self):
        self.username = None
        self.password = None
        self.user_id = None
        self.cur_account_number = None
        self.for_account_number = None
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
        DUM = 2
        db_connection = _connect_to_db()
        mycursor = db_connection.cursor()
        query = ('INSERT INTO foreign_account (account_number, foreign_account_balance, foreign_currency) VALUES (%s, %s, %s)')
        foreign_money = user_amount * DUM
        self.for_bank_balance += foreign_money
        mycursor.execute(query, (self.cur_account_number, self.for_bank_balance, 'DUM'))
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
    def get_foreign_account(self):
        db_connection = _connect_to_db()
        mycursor = db_connection.cursor()
        query = ('SELECT * FROM foreign account WHERE foreign_account_number = %')
        mycursor.execute(query, (self.cur_account_number,))
        self.for_account_number = foreign_account_number
        


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
user.xchange_transaction()
user.reset_user()
