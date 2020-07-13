# Credits to @Bablofil https://github.com/Bablofil/binance-api
import time
import json
import urllib
import hmac, hashlib
import requests

from urllib.parse import urlparse, urlencode
from urllib.request import Request, urlopen

class Binance():
    
    methods = {
            #  Public methods     
            'ping':             {'url': 'ping', 'method': 'GET', 'private': False},                     
            'time':             {'url': 'time', 'method': 'GET', 'private': False},         
            'exchangeInfo':     {'url': 'exchangeInfo', 'method': 'GET', 'private': False},
            'depth':            {'url': 'depth', 'method': 'GET', 'private': False},
            'trades':           {'url': 'trades', 'method': 'GET', 'private': False},  
            'historicalTrades': {'url': 'historicalTrades', 'method': 'GET', 'private': False},  
            'aggTrades':        {'url': 'aggTrades', 'method': 'GET', 'private': False},
            'klines':           {'url': 'klines', 'method': 'GET', 'private': False},   
            'avgPrice':         {'url': 'avgPrice', 'method': 'GET', 'private': False}, 
            'ticker24hr':       {'url': 'ticker/24hr', 'method': 'GET', 'private': False},
            'tickerPrice':      {'url': 'ticker/price', 'method': 'GET', 'private': False},   
            'tickerBookTicker': {'url': 'ticker/bookTicker', 'method': 'GET', 'private': False}, 
            #  Private methods   
            'createOrder':      {'url': 'order', 'method': 'POST', 'private': True},                        
            'testOrder':        {'url': 'test', 'method': 'POST', 'private': True},              
            'orderInfo':        {'url': 'order', 'method': 'GET', 'private': True},
            'cancelOrder':      {'url': 'order', 'method': 'DELETE', 'private': True},
            'openOrders':       {'url': 'openOrders', 'method': 'GET', 'private': True}, 
            'allOrders':        {'url': 'allOrders', 'method': 'GET', 'private': True},     
            'account':          {'url': 'account', 'method': 'GET', 'private': True}, 
            'myTrades':         {'url': 'myTrades', 'method': 'GET', 'private': True}, 
   }
    
    def __init__(self, API_KEY, API_SECRET):
        self.API_KEY = API_KEY
        self.API_SECRET = bytearray(API_SECRET, encoding='utf-8')
        self.shift_seconds = 0

    def __getattr__(self, name):
        def wrapper(*args, **kwargs):
            kwargs.update(command=name)
            return self.call_api(**kwargs)
        return wrapper

    def set_shift_seconds(self, seconds):
        self.shift_seconds = seconds
        
    def call_api(self, **kwargs):

        command = kwargs.pop('command')
        api_url = 'https://api.binance.com/api/v3/' + self.methods[command]['url']

        payload = kwargs
        headers = {}
        
        payload_str = urllib.parse.urlencode(payload)
        if self.methods[command]['private']:
            payload.update({'timestamp': int(time.time() + self.shift_seconds - 1) * 1000})
            payload_str = urllib.parse.urlencode(payload).encode('utf-8')
            sign = hmac.new(
                key=self.API_SECRET,
                msg=payload_str,
                digestmod=hashlib.sha256
            ).hexdigest()

            payload_str = payload_str.decode("utf-8") + "&signature="+str(sign) 
            headers = {"X-MBX-APIKEY": self.API_KEY}

        if self.methods[command]['method'] == 'GET':
            api_url += '?' + payload_str

        # print(api_url, payload_str, self.methods[command])
        response = requests.request(
            method=self.methods[command]['method'], 
            url=api_url, 
            data="" if self.methods[command]['method'] == 'GET' else payload_str,
            headers=headers)

        if 'code' in response.text:
            print(response.text)
            response = response.json()
            return response['error']
        return response.json()