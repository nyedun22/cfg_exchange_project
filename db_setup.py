import mysql.connector
from config import *
from mysql.connector import Error

mydb = mysql.connector.connect(
    host= HOST,
    user= USER,
    passwd= PASSWORD,
)

create_db_cursor = mydb.cursor()
create_db_cursor.execute(f"DROP DATABASE {DATABASE_NAME}")
create_db_cursor.execute(f"CREATE DATABASE {DATABASE_NAME}")
create_db_cursor.close()

try:
    connection = mysql.connector.connect(host= HOST,
                                         database= DATABASE_NAME,
                                         user= USER,
                                         password= PASSWORD)
    if connection.is_connected():
        cursor = connection.cursor()
        cursor.execute("CREATE TABLE user_details(user_ID INTEGER(10) NOT NULL UNIQUE AUTO_INCREMENT, first_name VARCHAR(255) NOT NULL, last_name VARCHAR(255) NOT NULL, username VARCHAR(255) NOT NULL UNIQUE, email VARCHAR(255) NOT NULL UNIQUE, pass_word CHAR(30) NOT NULL, address_line_1 VARCHAR(255) NOT NULL, postcode INTEGER(7), PRIMARY KEY (user_ID))")
        cursor.execute("CREATE TABLE bank_details (account_number INTEGER(8) NOT NULL UNIQUE AUTO_INCREMENT, user_ID INTEGER(10) NOT NULL, sort_code CHAR(8) NOT NULL, currency CHAR(3) NOT NULL, main_account_balance NUMERIC(20,2), PRIMARY KEY (account_number), FOREIGN KEY (user_ID) REFERENCES user_details(user_ID))")
        cursor.execute("CREATE TABLE foreign_account(foreign_account_number INTEGER(8) NOT NULL UNIQUE AUTO_INCREMENT, account_number INTEGER(8) NOT NULL, foreign_account_balance NUMERIC(20,2) NOT NULL, foreign_currency CHAR(3) NOT NULL, PRIMARY KEY (foreign_account_number), FOREIGN KEY (account_number) REFERENCES bank_details(account_number))")
        cursor.execute("CREATE TABLE transactions(transaction_ID INTEGER(20) NOT NULL UNIQUE AUTO_INCREMENT, account_number INTEGER(8) NOT NULL UNIQUE, foreign_account_number INTEGER(8) NOT NULL UNIQUE, date DATETIME NOT NULL, foreign_currency CHAR (3) NOT NULL, gbp_amount NUMERIC(20,2), foreign_currency_amount NUMERIC(20,2), exchange_rate NUMERIC(10,6), PRIMARY KEY (transaction_ID), FOREIGN KEY (account_number) REFERENCES bank_details(account_number), FOREIGN KEY (foreign_account_number) REFERENCES foreign_account(foreign_account_number))")
        cursor.execute("CREATE TABLE currency_codes(currency_ID CHAR(3), currency_name VARCHAR(255), PRIMARY KEY (currency_ID))")
except Error as e:
    print("Error while connecting to MySQL", e)
finally:
    if connection.is_connected():
        cursor.close()
        connection.close()