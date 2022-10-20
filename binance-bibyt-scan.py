from pybit import HTTP
from pybit import spot
from pybit import inverse_perpetual 
import time

from binance import Client, ThreadedWebsocketManager, ThreadedDepthCacheManager
from binance.enums import *
from binance.exceptions import BinanceAPIException
from requests import ReadTimeout, ConnectTimeout, HTTPError, Timeout, ConnectionError

# Ключи binance
api_key = "#################"
api_secret = "#################"
client = Client(api_key, api_secret)
currency_pair = "BTCUSDT"

session_unauth = HTTP(endpoint='https://api.bybit.com')
session = spot.HTTP(endpoint='https://api.bybit.com')

list_bybit = ["BTCUSDT", "ETHUSDT", "LTCUSDT", "TRXUSDT", "ADAUSDT", "SOLUSDT", "ATOMUSDT", "BNBUSDT", "NEOUSDT", "QTUMUSDT", "EOSUSDT", "IOTAUSDT",
"XLMUSDT", "ONTUSDT", "ETCUSDT", "ICXUSDT", "VETUSDT", "WAVESUSDT", "BTTUSDT", "HOTUSDT", "ZILUSDT", "ZRXUSDT", "BATUSDT", "XMRUSDT", "ZECUSDT", "IOSTUSDT", "CELRUSDT", 
"DASHUSDT", "OMGUSDT", "THETAUSDT", "ENJUSDT", "MATICUSDT", "ONEUSDT", "DUSKUSDT"]

difference_course = float(0.2)
print("Минимальный процент разности: ", str(difference_course), str("%"))

def scan():
    
    status = True

    while status:

        try:
            
            list_index_enumeration = 0
            list_index_bybit = 0
            list_binance_price = []

            course_get_all_tickers = client.get_all_tickers()
            binance_enumeration = True

            try:

                while binance_enumeration:

                    course_binance = course_get_all_tickers[list_index_enumeration]
                    course_symbol = course_binance['symbol']

                    if course_symbol == list_bybit[list_index_bybit]:

                        # print(course_symbol)
                        course_price = float(course_binance['price'])
                        # print(course_price)
                        list_index_bybit += 1
                        list_index_enumeration = 0
                        list_binance_price.append(course_price)
                        
                    if course_symbol != list_bybit[list_index_bybit]:

                        list_index_enumeration += 1 

            except IndexError:
                
                 binance_enumeration = False
                 print(list_binance_price)

            list_index_enumeration = 0
            list_index_bybit = 0
            list_bybit_price = []

            course_get_all_tickers = session_unauth.latest_information_for_symbol()
            # print(course_get_all_tickers)
            # break
            # print(course_get_all_tickers)

            bybit_enumeration = True

            try:

                while bybit_enumeration:

                    course_bybit = course_get_all_tickers['result'][list_index_enumeration]
                    course_symbol = course_bybit['symbol']                

                    if course_symbol == list_bybit[list_index_bybit]:

                        # print(course_symbol)
                        course_price = float(course_bybit['mark_price'])
                        # print(course_price)
                        list_index_bybit += 1
                        list_index_enumeration = 0
                        list_bybit_price.append(course_price)
                        
                    if course_symbol != list_bybit[list_index_bybit]:

                        list_index_enumeration += 1 

            except IndexError:
            
                bybit_enumeration = False
                print(list_bybit_price)
        
            # Калькулятор
            list_index_calculator = 0
            calculator = True

            try:

                while calculator:

                    if list_bybit_price[list_index_calculator] + (list_bybit_price[list_index_calculator] / 100 * difference_course) < list_binance_price[list_index_calculator]:
                    # if list_binance_price[list_index_calculator] + (list_binance_price[list_index_calculator] / 100 * difference_course) < list_bybit_price[list_index_calculator]:

                        print("---------------------------------------")
                        print("Пара: ", list_bybit[list_index_calculator])
                        print("Курс Бинанс: ", list_binance_price[list_index_calculator])
                        print("Курс Байбит: ", list_bybit_price[list_index_calculator])
                        list_index_calculator += 1
                    
                    else:
                    
                        list_index_calculator += 1

            except IndexError:
            
                calculator = False


        except BinanceAPIException as e:

            print("Ошибка: BinanceAPIException")
            time.sleep(3)

        except (ConnectTimeout, HTTPError, ReadTimeout, Timeout, ConnectionError):

            print("Ошибка: ConnectTimeout")
            time.sleep(3)

scan()
