import requests
from datetime import datetime
from pprint import pprint as pp


url = 'https://v6.exchangerate-api.com/v6/867729e3b3de9dca04462186/latest/GBP'

r = requests.get(url)
print(r.status_code)
data = r.json()
# pp(data) # Returns all the data from the API

class currency():
    def __init__(self):
        self.rate = 0
        self.foreign_amount = 0
        self.currency_code = ''

    def get_rate(self):
        """
        Allows the user to select the desired currency, and returns the exchange rate from GBP along with a timestamp for the date of transaction
        """
        self.currency_code = str(input("Enter currency code: ")) # Could we make this a dropdown menu?
        if r.status_code == 200:
            self.output = r.json()
            self.rate = (self.output['conversion_rates'][self.currency_code])
            print(self.rate)
            ts = datetime.now() #timestamp
            print('at ',(ts.strftime('%I:%M:%S, %d/%m/%Y')))

    def exchange_amount(self):
        """
        The user then inputs the amount to be exchanged, which shows as eg 100 GDP = 119.72 USD (rounded to 2 dp)
        """
        enter_amount = int(input("Enter amount: £"))
        foreign_amount = (enter_amount * (self.rate))
        print(f'{enter_amount} GDP = ')
        print (round(foreign_amount,2), self.currency_code)


c = currency()
c.get_rate()
c.exchange_amount()



