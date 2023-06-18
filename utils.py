#!/usr/bin/env python

import requests
import json
from config import keys

quote_ticker = ''
base_ticker = ''


class ConvertionException(Exception):
    pass


class CryptoConverter:
    @staticmethod
    def convert(quote: str, base: str, amount: str):
        global quote_ticker
        global base_ticker

        try:
            for k, v in keys.items():
                if v[0] == quote:
                    quote_ticker = k
        except KeyError:
            raise ConvertionException(f'Не удалось обработать валюту {quote_ticker}')

        try:
            for k, v in keys.items():
                if v[0] == base:
                    base_ticker = k

        except KeyError:
            raise ConvertionException(f'Не удалось обработать валюту {base_ticker}')

        if quote == base:
            raise ConvertionException(f'Невозможно перевести одинаковые валюты {base_ticker}.')

        try:
            amount = float(amount)
        except ValueError:
            raise ConvertionException(f'Не удалось обработать количество {amount}')

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}')
        total = json.loads(r.content)[base_ticker]
        total_base = total * amount
        return total_base
