from poloniex import Poloniex
from datetime import datetime
import time
"""
Poloniex bot that buys 0.001 EXP every X secs
"""

SECS = 60
AMT = 1
CURRENCY = "EXP"
MIN_BALANCE = AMT
TICKER = 'BTC_{currency}'.format(currency=CURRENCY)

# polo
polo = Poloniex(extend=True)
# API KEY
polo.Key = 1111  # to be filled
polo.Secret = 11111  # to be filled

TIME = time.time() - SECS
# for checking the balance in the first iteration
currentPrice = polo.returnOrderBook(TICKER, depth=5)["asks"][0][0]

balance = polo.returnBalances()
if "error" in balance:
    print(balance["error"])
    exit()
else:
    print("Your BTC balance is {amt}".format(amt=balance["BTC"]))

while True:
    if time.time() - TIME >= SECS:
        # check balance
        balanceInBTC = polo.returnBalances()["BTC"]
        # if amount of BTC cannot buy AMT * 10 coins, don't buy
        if float(balanceInBTC) < MIN_BALANCE * float(currentPrice):
            print("Insufficient balance in BTC to buy {amt} {cur}. Balance: {bal}. Price of {cur}: {price}".format(
                bal=balanceInBTC, cur=CURRENCY,
                price=currentPrice, amt=MIN_BALANCE))
        else:
            isBought = False
            # while order hasnt gone through
            while not isBought:
                currentPrice = polo.returnOrderBook(
                    TICKER, depth=5)["asks"][0][0]


                order = polo.buy(TICKER, currentPrice, AMT)
                print(order)

                # if order goes through
                if "orderNumber" in order.keys():
                    # get current datetime
                    dt = datetime.utcnow().strftime(
                        "%y-%m-%d %H:%M:%S {tz}".format(tz=time.tzname[0]))

                    print("{amt} {cur} has been bought @ {price} || {dt}".format(
                        amt=AMT, cur=CURRENCY, price=currentPrice, dt=dt))
                    # order goes through
                    isBought = True

        # reset timer
        TIME = time.time()
