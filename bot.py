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

# Parameters

target_diff = 0.4  # 이 값 이상 차이날 경우 알림 (단위 : %)
target_volume = 100000  # 이 값 이상 거래할 수 있을때만 알림 (단위 : KRW)
time_interval = 10  # 반복 주기 (단위 : 초)
coins = ["BTC", "ETH", "XRP", "BCH", "EOS"]  # 관찰할 코인 리스트

# Define Functions


def telegram_send(text):
    bot.sendMessage(chat_id=chat_id, text=text)
    print(text)


def diff(num1, num2):
    return round((num1 - num2) / num2 * 100, 2)


def run_bot():
    # Load Bithumb Orderbook
    print("Loading Bithumb Orderbook")
    api_url_bithumb = "https://api.bithumb.com/public/orderbook/all"
    bithumb_orderbook_response = requests.get(api_url_bithumb)
    bithumb_orderbook_result = json.loads(bithumb_orderbook_response.text)

    # Get First Bid Ask Price and Quantity at Bithumb
    bithumb_bid = []
    bithumb_bid.append(bithumb_orderbook_result["data"]["BTC"]["bids"][0])
    bithumb_bid.append(bithumb_orderbook_result["data"]["ETH"]["bids"][0])
    bithumb_bid.append(bithumb_orderbook_result["data"]["XRP"]["bids"][0])
    bithumb_bid.append(bithumb_orderbook_result["data"]["BCH"]["bids"][0])
    bithumb_bid.append(bithumb_orderbook_result["data"]["EOS"]["bids"][0])

    bithumb_ask = []
    bithumb_ask.append(bithumb_orderbook_result["data"]["BTC"]["asks"][0])
    bithumb_ask.append(bithumb_orderbook_result["data"]["ETH"]["asks"][0])
    bithumb_ask.append(bithumb_orderbook_result["data"]["XRP"]["asks"][0])
    bithumb_ask.append(bithumb_orderbook_result["data"]["BCH"]["asks"][0])
    bithumb_ask.append(bithumb_orderbook_result["data"]["EOS"]["asks"][0])

    # Load Upbit Orderbook
    print("Loading Upbit Orderbook")
    api_url_upbit_BTC = "https://api.upbit.com/v1/orderbook?markets=KRW-BTC"
    upbit_orderbook_BTC_response = requests.get(api_url_upbit_BTC)
    upbit_orderbook_BTC_result = json.loads(upbit_orderbook_BTC_response.text)

    api_url_upbit_ETH = "https://api.upbit.com/v1/orderbook?markets=KRW-ETH"
    upbit_orderbook_ETH_response = requests.get(api_url_upbit_ETH)
    upbit_orderbook_ETH_result = json.loads(upbit_orderbook_ETH_response.text)

    api_url_upbit_XRP = "https://api.upbit.com/v1/orderbook?markets=KRW-XRP"
    upbit_orderbook_XRP_response = requests.get(api_url_upbit_XRP)
    upbit_orderbook_XRP_result = json.loads(upbit_orderbook_XRP_response.text)

    api_url_upbit_BCH = "https://api.upbit.com/v1/orderbook?markets=KRW-BCH"
    upbit_orderbook_BCH_response = requests.get(api_url_upbit_BCH)
    upbit_orderbook_BCH_result = json.loads(upbit_orderbook_BCH_response.text)

    api_url_upbit_EOS = "https://api.upbit.com/v1/orderbook?markets=KRW-EOS"
    upbit_orderbook_EOS_response = requests.get(api_url_upbit_EOS)
    upbit_orderbook_EOS_result = json.loads(upbit_orderbook_EOS_response.text)

    # Get First Bid Ask Price and Quantity at Upbit
    upbit_orderbook = []
    upbit_orderbook.append(upbit_orderbook_BTC_result[0]["orderbook_units"][0])
    upbit_orderbook.append(upbit_orderbook_ETH_result[0]["orderbook_units"][0])
    upbit_orderbook.append(upbit_orderbook_XRP_result[0]["orderbook_units"][0])
    upbit_orderbook.append(upbit_orderbook_BCH_result[0]["orderbook_units"][0])
    upbit_orderbook.append(upbit_orderbook_EOS_result[0]["orderbook_units"][0])

    # Arbitrage Decision between Bithumb and Upbit
    # Step 1. Bithumb Ask vs. Upbit Bid (Buy at Bithumb and Sell at Upbit)
    for i in range(len(bithumb_ask)):
        bithumb_ask_price = int(bithumb_ask[i]["price"])
        bithumb_ask_quantity = float(bithumb_ask[i]["quantity"])
        upbit_bid_price = int(upbit_orderbook[i]["bid_price"])
        upbit_bid_quantity = float(upbit_orderbook[i]["bid_size"])
        available_size = int(round(min(bithumb_ask_quantity,
                                       upbit_bid_quantity) * bithumb_ask_price))
        difference = diff(upbit_bid_price, bithumb_ask_price)

        if difference > target_diff and available_size > target_volume:
            text = "[%s] 기회 발생\n빗썸 매수 : %s / %s %s\n업비트 매도 : %s / %s %s\n차이 : %s%%\n거래 가능 규모 : %s원" % (
                coins[i], bithumb_ask_price, bithumb_ask_quantity, coins[i], upbit_bid_price, upbit_bid_quantity, coins[i], difference, available_size)
            telegram_send(text)

    # Step 1. Bithumb Bid vs. Upbit Ask (Buy at Upbit and Sell at Bithumb)
    for i in range(len(bithumb_bid)):
        bithumb_bid_price = int(bithumb_bid[i]["price"])
        bithumb_bid_quantity = float(bithumb_bid[i]["quantity"])
        upbit_ask_price = int(upbit_orderbook[i]["ask_price"])
        upbit_ask_quantity = float(upbit_orderbook[i]["ask_size"])
        available_size = int(round(min(bithumb_bid_quantity,
                                       upbit_ask_quantity) * upbit_ask_price))
        difference = diff(bithumb_bid_price, upbit_ask_price)

        if difference > target_diff and available_size > target_volume:
            text = "[%s] 기회 발생\n업비트 매수 : %s / %s %s\n빗썸 매도 : %s / %s %s\n차이 : %s%%\n거래 가능 규모 : %s원" % (
                coins[i], upbit_ask_price, upbit_ask_quantity, coins[i], bithumb_bid_price, bithumb_bid_quantity, coins[i], difference, available_size)
            telegram_send(text)


# Running Part


while True:
    run_bot()
    time.sleep(time_interval)

print("Done.")
