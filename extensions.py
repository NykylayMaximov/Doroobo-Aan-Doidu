import requests
import json
from config import currents


class ConvertionException(Exception):
    pass

class Converter:
    @staticmethod
    def converter(text_value: str):

        if len(text_value) != 3:
            raise ConvertionException('Слишком много или мало параметров')

        first, second, amount = text_value

        try:
            amount = float(amount)
        except ValueError:
            raise ConvertionException('Не корректные данные количества валюты')

        if first == second:
            raise ConvertionException('Невозможно конвертировать одинаковые валюты')

        currents_tickers = [k for k in currents.keys()]

        if first not in currents_tickers or second not in currents_tickers:
            raise ConvertionException('Не корректные данные валюты')

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={currents[first]}&tsyms={currents[second]}')
        result = json.loads(r.content)[currents[second]]
        text = f"{round(amount, 2)} {currents[first]} = {round(amount * result, 2)} {currents[second]}"

        return text