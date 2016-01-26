#!/usr/bin/python

import hashlib
import hmac
import time
import urllib
from btcutil import Market, Course
from requests import Session, Request

API_KEY = 'MY_API_KEY'
API_SECRET = '5uP3r5eCrE7'
BASE_URI = 'https://api.bitcoin.de/v1/'
HTTP_GET = 'GET'
HTTP_POST = 'POST'
HTTP_DELTE = 'DELETE'
nonce = time.time()


class API_ENDPOINTS:

    ORDERS = 'orders'
    TRADES = 'trades'
    ACCOUNT = 'account'
    RATES = 'rates'
    LEDGER = 'account/ledger'


def custom_request(method, endpoint, params=None):
    request = Request(method, BASE_URI+endpoint, params=params)
    prepped = request.prepare()
    prepped.headers = build_header(request)
    return prepped


def rebuild_request(request):
    request.headers = build_header(request)


def showOrderbookRequest(parameters):
    if 'type' not in parameters:
        return
    return custom_request(HTTP_GET, API_ENDPOINTS.ORDERS, parameters)


def showOrderbookCompactRequest():
    return custom_request(HTTP_GET, API_ENDPOINTS.ORDERS+'/compact')


def createOrderRequest(parameters):
    if ('type' not in parameters or 'max_amount' not in parameters or
            'price' not in parameters):
        return
    return custom_request(HTTP_POST, API_ENDPOINTS.ORDERS, parameters)


def deleteOrderRequest(paramers):
    if 'order_id' not in paramers:
        return
    return custom_request(HTTP_DELTE, API_ENDPOINTS.ORDERS, paramers)


def showMyOrdersRequest(parameters=None):
    if parameters:
        return custom_request(HTTP_GET, API_ENDPOINTS.ORDERS, parameters)
    return custom_request(HTTP_GET, API_ENDPOINTS.ORDERS)


def showMyOrderDetailsRequest(parameters):
    if 'order_id' not in parameters:
        return
    return custom_request(HTTP_GET, API_ENDPOINTS.ORDERS, parameters)


def executeTradeRequest(parameters):
    if ('order_id' not in parameters or 'type' not in parameters or
            'amount' not in parameters):
        return
    return custom_request(HTTP_POST, API_ENDPOINTS.TRADES, parameters)


def showMyTradesRequest(parameters):
    return custom_request(HTTP_GET, API_ENDPOINTS.TRADES, parameters)


def showMyTradeDetaislRequest(parameters):
    if 'trade_id' not in parameters:
        return
    return custom_request(HTTP_GET, API_ENDPOINTS.TRADES, parameters)


def showRatesRequest():
    return custom_request(HTTP_GET, API_ENDPOINTS.RATES, None)


def build_header(request):
    global nonce
    if request.params:
        uri = request.url+'?'+urllib.urlencode(request.params)
    else:
        uri = request.url
    md5param = build_md5(request)
    method = request.method
    hmac = build_hmac(method, uri, md5param, nonce)
    header = {'X-API-KEY': API_KEY,
              'X-API-NONCE': nonce,
              'X-API-SIGNATURE': hmac}
    nonce += 1
    return header


def build_hmac(method, uri, md5param, nonce):
    string = method+'#'+uri+'#'+API_KEY+'#'+str(nonce)+'#'+md5param
    sha256 = hmac.new(key=API_SECRET, msg=string,
                      digestmod=hashlib.sha256).hexdigest()
    return sha256


def build_md5(request):
    if request.method != HTTP_POST or request.params is None:
        return 'd41d8cd98f00b204e9800998ecf8427e'
    else:
        url = urllib.urlencode(request.params)
        url = url.encode('utf-8')
        return hashlib.md5(url).hexdigest()


def allBuyOrders():
    params = {'type': 'buy', 'only_express_orders': 1, 'only_kyc_full': 1}
    return showOrderbookRequest(params)


def allSellOrders():
    params = {'type': 'sell', 'only_express_orders': 1, 'only_kyc_full': 1}
    return showOrderbookRequest(params)


def main():
    session = Session()
    marketReq = showOrderbookCompactRequest()
    ratesReq = showRatesRequest()

    market = Market(session.send(marketReq).json())
    rates = session.send(ratesReq).json()
    course = Course(rates)
    print "---------------------------------------------"
    print "\t[*] Asks [*]"
    print "\tvolume: %f" % market.get_BidVolume()
    print "\tmedian price: %f" % market.get_BidMedian()
    print "\tavg price: %f" % market.get_BidAverage()
    print "\tcheapest: %f" % market.get_BidLowest()
    print "\tmost expensive: %f" % market.get_BidHighest()
    print "---------------------------------------------"
    print "\t[*] Bid [*]"
    print "\tvolume: %f" % market.get_AskVolume()
    print "\tmedian price: %f" % market.get_AskMedian()
    print "\tavg price: %f" % market.get_AskAverage()
    print "\thighest bid: %f" % market.get_AskHighest()
    print "\tlowest bid: %f" % market.get_AskLowest()
    print "---------------------------------------------"
    print "\t[*] courses [*]"
    print "\texact: %f" % course.getCurrentRate()
    print "\t12 Hours: %f" % course.get12hWeighted()
    print "\t3 hours: %f" % course.get3hWeighted()

if __name__ == '__main__':
    main()
