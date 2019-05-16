import requests
from urllib.parse import urlparse, urlencode, urlunparse
import sys
import portfolio

class Investment():
    def __init__(self):
        self.connect = requests.Session()
        self.token = {'token':'Tsk_52fad3a049dd4719bfbe7034282a1cd5'}
        self.iex_url = 'https://sandbox.iexapis.com/'

    def __buildURL(self, base, path, query):
        '''query = {'key':'value1, value2'}'''
        deconstructed_base = list(urlparse(base)) #scheme netloc path params[x] query fragment[x]
        deconstructed_base[2] = path
        deconstructed_base[4] = urlencode(query)
        return urlunparse(deconstructed_base)

    def getCurrentPrice(self, ticker):
        """get current price (during hours) information of ticker""" #add real time?
        path = '/'.join(['stable','stock', ticker, 'price'])
        query = self.token
        return self.connect.get(self.__buildURL(self.iex_url, path, query)).json()
        #return self.connect.get(self.iex_url+ticker+endpoint+self.token).json()
        #if ticker doesnt exist...
    
    def getCompanyName(self, ticker):
        pass

    def getEarningsReportDate(self, ticker):
        """get upcoming earnings report date information of ticker"""
        path = '/'.join(['stable','stock', ticker, 'estimates'])
        query = self.token
        return self.connect.get(self.__buildURL(self.iex_url, path, query)).json()['estimates'][0]['reportDate']

    def getUpcomingERs(self, num):
        """get list of num companies upcoming earnings report date"""
        path = '/'.join(['stable','stock', ticker, 'batch'])
        # return self.connect.get(self.iex_url+endpoint+)
    

if __name__ == "__main__":
    portfolio = portfolio.InvestmentPortfolio()
    stock = Investment()
    commands = []
    
    #print(urlencode())
    #print(stock.buildURL('https://sandbox.iexapis.com/', '/stable/stock/market/batch', {'symbols':'aapl,fb,tsla', 'types':'quote,news,chart', 'range':'1m', 'last':'5', 'token':'Tsk_52fad3a049dd4719bfbe7034282a1cd5'}))
    #print(stock.buildURL('https://sandbox.iexapis.com/stable/stock/market/batch?symbols=aapl,fb,tsla&types=quote,news,chart&range=1m&last=5&token=Tsk_52fad3a049dd4719bfbe7034282a1cd5'))
    if len(sys.argv) > 1:
        ticker = sys.argv[1]
        payload = sys.argv[2]
        print(stock.getCurrentPrice(ticker))
        print(stock.getEarningsReportDate(ticker))