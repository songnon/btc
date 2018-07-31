#!/usr/bin/env python

import time, threading, requests

# Assume the transacton fee is 0.8%
BTC_TRANSACTION_FEE = 0.0008

def main():
    # print(time.ctime())
    otc_huobi_url = "https://otc-api.huobi.com/v1/data/trade-market?country=37&currency=1&payMethod=0&currPage=1&coinId=1&tradeType=sell&blockType=general&online=1"
    r = requests.get(otc_huobi_url)
    data = r.json().get("data")
    if data:
        # print(data)
        # sort the data based on 'price'
        data = list(filter(lambda x: x.get('price', 0) > 0 and x['minTradeLimit'] <= 5000, data))
        data.sort(key=lambda x: x.get('price'))
        # print(data[0])
        otc_price = data[0]['price']
        otc_volume = data[0]['tradeCount']
        # print(otc_price, ':', time.ctime())

    btc_market_url = "https://api.btcmarkets.net/market/BTC/AUD/orderbook"
    btc_market_r = requests.get(btc_market_url)
    # print(btc_market_r.json())
    btc_market_bids = btc_market_r.json().get("bids", [])
    if len(btc_market_bids) > 0:
        btc_market_price, btc_market_volume = btc_market_bids[0]
        # print(btc_market_price)
    if otc_price and btc_market_price:
        print("{:.2f}, {:.2f}, {:.3f}, {:.3f}, {}".format(
            otc_price,
            btc_market_price,
            otc_price / btc_market_price,
            otc_price / (btc_market_price * (1 - BTC_TRANSACTION_FEE)),
            time.ctime()))
    threading.Timer(120, main).start()
    

if __name__ == '__main__':
    main()
