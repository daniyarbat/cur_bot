import requests
import json
from datetime import datetime
import os

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

    try:
        response = requests.get(url, headers={'apikey': API_KEY}, params={'base': base} )
        response.raise_for_status()  # Raises an HTTPError for bad responses

        rate = response.json ()['rates']['KZT']
        return rate
    except requests.exceptions.HTTPError as http_err:
        print ( f"HTTP error occurred: {http_err}" )
    except Exception as e:
        print(f"Error getting currency rate: {e}")
        return None


def save_to_json(data: dict) -> None:
    '''
    Saves data to JSON
    :param data: dict
    :return: JSON file
    '''

    try:
        with open(CURRENCY_RATES_FILE, 'a') as file:
            if os.stat(CURRENCY_RATES_FILE).st_size == 0:
                json.dump([data], file)
            else:
                with open(CURRENCY_RATES_FILE, 'r') as file:
                    data_list = json.load(file)
                    data_list.append(data)
                with open(CURRENCY_RATES_FILE, 'w') as file:
                    json.dump(data_list, file, indent=2)
    except Exception as e:
        print(f"Error saving to JSON: {e}")

if __name__ == '__main__':
    main()
