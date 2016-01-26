#!/usr/bin/python


class Market():

    def __init__(self, market):
        self.market = market
        self.asks = market['orders']['asks']
        self.bids = market['orders']['bids']

    def get_asks(self):
        return self.asks

    def get_bids(self):
        return self.bids

    def get_avgPrice(self, prices):
        sum = 0.0
        for item in prices:
            sum += item
        return sum/len(prices)

    def get_medianPrice(self, prices):
        prices.sort()
        length = len(prices)
        if not length % 2:
            return (prices[length/2] + prices[length/2-1]) / 2.0
        else:
            return prices[(length/2)]

    def get_totalVolume(self, orders):
        total = 0.0
        for order in orders:
            total += order['amount']
        return total

    def get_lowest(self, prices):
        prices.sort()
        return prices[0]

    def get_highest(self, prices):
        prices.sort()
        return prices[-1]

    def strip_prices(self, orders):
        prices = []
        for order in orders:
            prices.append(order['price'])
        return prices

    def get_BidVolume(self):
        return self.get_totalVolume(self.bids)

    def get_AskVolume(self):
        return self.get_totalVolume(self.asks)

    def get_BidAverage(self):
        return self.get_avgPrice(self.strip_prices(self.bids))

    def get_AskAverage(self):
        return self.get_avgPrice(self.strip_prices(self.asks))

    def get_BidMedian(self):
        return self.get_medianPrice(self.strip_prices(self.bids))

    def get_AskMedian(self):
        return self.get_medianPrice(self.strip_prices(self.asks))

    def get_BidLowest(self):
        return self.get_lowest(self.strip_prices(self.bids))

    def get_AskLowest(self):
        return self.get_lowest(self.strip_prices(self.asks))

    def get_BidHighest(self):
        return self.get_highest(self.strip_prices(self.bids))

    def get_AskHighest(self):
        return self.get_highest(self.strip_prices(self.asks))


class Course():

    def __init__(self, course):
        self._rate = float(course['rates']['rate_weighted'])
        self._rate12 = float(course['rates']['rate_weighted_12h'])
        self._rate3 = float(course['rates']['rate_weighted_3h'])

    def getCurrentRate(self):
        return self._rate

    def get12hWeighted(self):
        return self._rate12

    def get3hWeighted(self):
        return self._rate3


class ExpressMarket():
    """ Only yields the top 20 filtered Express-Exchange Offers """
    def __init__(self, bids, asks):
        self.bids = bids
        self.asks = asks
