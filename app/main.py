import requests
from requests.exceptions import Timeout, ConnectionError

from fastapi import FastAPI

from app.const import URL, GET, KEY


app = FastAPI()


@app.get("/api/rates")
async def convector(
    c_from: str,
    to: str,
    value: int,

) -> dict[str, float]:
    """

    :param c_from: EUR
    :param to: RUB
    :param value: 6
    :return: 256.1231

    По ручке convector мы отправляем пару в соответсвии с докуменатцией внешнего API 'https://currate.ru/currency/list'
    По форме EURRUB, EURUSD и т.д
    Я сделал c_from потому что, from - служебное слово в python
    После отправки запроса на сайт с параметрами EURRUB, мне прилеает актуальный курс конвертации
    Который я умножаю на кол-во денег, которое нужно конвертировать

    P.S лучше держать ключь в .env файле, но у тогда бы вам пришлось заходить на сайт https://currate.ru/
    И генерировать свой ключь для API

    """
    params_api = {
        'get': GET,
        'pairs': f'{c_from}{to}',
        'key': KEY,
    }
    try:
        parsed_app_json = requests.get(
            URL, params=params_api
        ).json()
        coefficient = parsed_app_json['data'][f'{c_from}{to}']
    except TypeError:
        raise TypeError('Неверное написние валюты или кол-во денег')
    except Timeout:
        raise Timeout('Время запроса истекло')
    except ConnectionError:
        raise ConnectionError('Cетевая ошибка')
    return {"result": float(coefficient) * value}