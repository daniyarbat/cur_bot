import requests
import json
from datetime import datetime
import os
import pprint

API_KEY = os.getenv('APILAYER_KEY')
CURRENCY_RATES_FILE = 'currency_rates.json'


def main():

    while True:
        currency = input('Print currency name: USD, EUR ').upper().strip()

        currency_list = ['USD', 'EUR', 'RUB', 'CNY']

        if currency not in currency_list:
            print('Incorrect input')
            continue

        rate = get_currency_rate(currency)

        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        print(f'Course: {currency} to KZT: {rate}')

        data = {'currency': currency, 'rate': rate, 'times2tamp': timestamp}

        save_to_json(data)

        choice = input('Choose action: 1 - continue, 2 - quit ')

        if choice == '1':
            continue
        elif choice == '2':
            break
        else:
            print('Incorrect input')

def get_currency_rate(base: str) -> float:
    '''
    Gets course from API
    :param base: base currency
    :return: in float type
    '''

    url = "https://api.apilayer.com/exchangerates_data/latest"

    response = requests.get(url, headers={'apikey': API_KEY}, params={'base': base})

    rate = response.json()['rates']['KZT']

    return rate

def save_to_json(data: dict) -> None:
    '''
    Saves data to JSON
    :param data: dict
    :return: JSON file
    '''

    with open(CURRENCY_RATES_FILE, 'a') as file:
        if os.stat(CURRENCY_RATES_FILE).st_size == 0:
            json.dump([data], file)
        else:
            with open(CURRENCY_RATES_FILE, 'r') as file:
                data_list = json.load(file)
                data_list.append(data)
            with open(CURRENCY_RATES_FILE, 'w') as file:
                json.dump(data_list, file)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    main()
