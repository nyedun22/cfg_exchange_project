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
    


#function to get currency

def get_currencies():
    db_connection = _connect_to_db()
    mycursor = db_connection.cursor()
    currencies_query = ('SELECT * FROM currency_codes')
    mycursor.execute(currencies_query)
    results = mycursor.fetchall()
    return results
        # all_currencies = []
        # for currency in mycursor:
        #     # all_currencies.append(currency)
        #     print(currency)
        # return all_currencies

