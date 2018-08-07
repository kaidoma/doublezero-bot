# DoubleZero's Telegram Bot for Price Notification

# Developed by Kisung Nam (DoubleZero)

import telegram
import sys
import pprint
import json
import requests
import threading
import time

my_token = ''
chat_id = ''
print("Creating DoubleZero's Telegram Bot...")
bot = telegram.Bot(token=my_token)

# Target Values

target_diff = 0.5  # 이 값 이상 차이날 경우 알림

# Define Functions


def telegram_send(text):
    bot.sendMessage(chat_id=chat_id, text=text)
    print(text)


def diff(num1, num2):
    if num1 > num2:
        return round((num1 - num2) / num2 * 100, 2)
    else:
        return round((num2 - num1) / num1 * 100, 2)


def run_bot():
    print("Loading Bithumb Price")
    api_url_bithumb = "https://api.bithumb.com/public/ticker/all"
    resp = requests.get(api_url_bithumb)
    result = json.loads(resp.text)
    bithumb_BTC = int(float(result["data"]["BTC"]["closing_price"]))
    bithumb_ETH = int(float(result["data"]["ETH"]["closing_price"]))
    bithumb_XRP = int(float(result["data"]["XRP"]["closing_price"]))
    bithumb_BCH = int(float(result["data"]["BCH"]["closing_price"]))
    bithumb_EOS = int(float(result["data"]["EOS"]["closing_price"]))

    print("Loading Upbit Price")
    api_url_upbit_btc = "https://api.upbit.com/v1/ticker?markets=KRW-BTC"
    resp = requests.get(api_url_upbit_btc)
    result = json.loads(resp.text)
    upbit_BTC = int(float(result[0]["trade_price"]))

    api_url_upbit_eth = "https://api.upbit.com/v1/ticker?markets=KRW-ETH"
    resp = requests.get(api_url_upbit_eth)
    result = json.loads(resp.text)
    upbit_ETH = int(float(result[0]["trade_price"]))

    api_url_upbit_xrp = "https://api.upbit.com/v1/ticker?markets=KRW-XRP"
    resp = requests.get(api_url_upbit_xrp)
    result = json.loads(resp.text)
    upbit_XRP = int(float(result[0]["trade_price"]))

    api_url_upbit_bch = "https://api.upbit.com/v1/ticker?markets=KRW-BCH"
    resp = requests.get(api_url_upbit_bch)
    result = json.loads(resp.text)
    upbit_BCH = int(float(result[0]["trade_price"]))

    api_url_upbit_eos = "https://api.upbit.com/v1/ticker?markets=KRW-EOS"
    resp = requests.get(api_url_upbit_eos)
    result = json.loads(resp.text)
    upbit_EOS = int(float(result[0]["trade_price"]))

    difference_BTC = diff(bithumb_BTC, upbit_BTC)
    print(difference_BTC)
    difference_ETH = diff(bithumb_ETH, upbit_ETH)
    print(difference_ETH)
    difference_XRP = diff(bithumb_XRP, upbit_XRP)
    print(difference_XRP)
    difference_BCH = diff(bithumb_BCH, upbit_BCH)
    print(difference_BCH)
    difference_EOS = diff(bithumb_EOS, upbit_EOS)
    print(difference_EOS)

    text_BTC = "빗썸 BTC 가격 : %s \n업비트 BTC 가격 : %s \n차이 : %s%%" % (
        bithumb_BTC, upbit_BTC, difference_BTC)
    text_ETH = "빗썸 ETH 가격 : %s \n업비트 ETH 가격 : %s \n차이 : %s%%" % (
        bithumb_ETH, upbit_ETH, difference_ETH)
    text_XRP = "빗썸 XRP 가격 : %s \n업비트 XRP 가격 : %s \n차이 : %s%%" % (
        bithumb_XRP, upbit_XRP, difference_XRP)
    text_BCH = "빗썸 BCH 가격 : %s \n업비트 BCH 가격 : %s \n차이 : %s%%" % (
        bithumb_BCH, upbit_BCH, difference_BCH)
    text_EOS = "빗썸 EOS 가격 : %s \n업비트 EOS 가격 : %s \n차이 : %s%%" % (
        bithumb_EOS, upbit_EOS, difference_EOS)

    if difference_BTC > target_diff:
        telegram_send(text_BTC)

    if difference_ETH > target_diff:
        telegram_send(text_ETH)

    if difference_XRP > target_diff:
        telegram_send(text_XRP)

    if difference_BCH > target_diff:
        telegram_send(text_BCH)

    if difference_EOS > target_diff:
        telegram_send(text_EOS)


# Running Part

while True:
    run_bot()
    time.sleep(10)

print("Done.")
