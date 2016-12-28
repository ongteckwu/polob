from poloniex import Poloniex
from datetime import datetime
import time
"""
Poloniex bot that buys 0.001 EXP every X secs
"""

SECS = 60
AMT = 0.0001
CURRENCY = "EXP"
TICKER = 'BTC_{currency}'.format(currency=CURRENCY)

# polo
polo = Poloniex(extend=True, coach=True)
# API KEY
polo.KEY = 1111  # to be filled
polo.SECRET = 1111  # to be filled

TIME = time.time()

while True:
    if time.time() - TIME >= SECS:
        isBought = False
        # while order hasnt gone through
        while not isBought:
            currentPrice = polo.returnOrderBook(TICKER, depth=5)["asks"][0][0]
            order = polo.buy(TICKER, currentPrice, AMT)

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
