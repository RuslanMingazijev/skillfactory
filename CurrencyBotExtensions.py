import json
import requests
from CurrencyConfig import keys


class ConversionException(Exception):
    pass


class CurrencyConverter:
    @staticmethod
    def convert(quote: str, base: str, amount: str):
        if quote == base:
            raise ConversionException(f'Same currencies selected: {quote}')

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise ConversionException(f'Could not process the currency {quote}')

        try:
            base_ticker = keys[base]
        except KeyError:
            raise ConversionException(f'Could not process the currency {base}')

        try:
            amount != float(amount)
        except ValueError:
            raise ConversionException(f'Could not process the amount {amount}')

        r = requests.get(
            f'https://v6.exchangerate-api.com/v6/6abc60cfa9152c9ede480636/pair/{quote_ticker}/{base_ticker}/{amount}'
        )
        total_base = json.loads(r.content)['conversion_result']

        return total_base
