import pandas as pd
import glob
import os
from utils import *

from pandas_datareader.data import DataReader
from datetime import datetime
from dateutil.relativedelta import relativedelta
import requests, io
from urllib.parse import urlparse
import textract


def hash_tickers(stocks):
    return fast_hash(' '.join(sorted(stocks)), 'dsb8jk21ijdidwdhjhj')

def round_datetime(dtme):
    return datetime(dtme.year, dtme.month, dtme.day)

class Loader():

    def __init__(self, url, report_type):
        self.url = url
        self.report_type = report_type

    def load(self):

        handlers = {
            'csv': self.HandleCsv,
            'xls': self.HandleXls,
            'pdf': self.HandlePdf,
            'txt': self.HandleTxt
        }

        return handlers[self.report_type]()

    @property
    def data(self):
        if self.is_cached():
            self.load_from_cache()
        else:
            self.load_from_remote()
            self.to_cache()

    def load_from_cache(self):
        pass

    def load_from_remote(self):
        pass

    def to_cache(self):
        pass

    def is_cached(self):
        pass

    def get_cache_info(self):
        pass

    def HandleCsv(self):
        return requests.get(self.url, allow_redirects=True).text

    def HandleXls(self):
        return get_df_from_ExcelFile(self.url).to_csv(None, sep=';', encoding='utf-8')

    def HandlePdf(self):
        a = urlparse(self.url)
        filename = os.path.basename(a.path)
        download(self.url, filename)
        return textract.process(filename).decode("utf8")

    def HandleTxt(self):
        pass


class UniverseLoader(Loader):

    def __init__(self, config, universe_code, period):

        self.stocks = config['universe'][universe_code]['holdings'].keys()

        self.end = self.round_datetime(datetime.now())
        self.start = self.end - relativedelta(months=period)

        if self._is_cached():
            self._load_from_cache()
        else:
            self._load_from_web()
            self._cache_universe()

    @property
    def data(self):
        if self.is_cached():
            self.load_from_cache()
        else:
            self.load_from_remote()
            self.to_cache()

    def load_from_cache(self):
        print("loading data from cache")
        cache = self.get_cache()
        hash_ = str(hash_tickers(self.stocks))
        ds_ = pd.read_pickle("cache__{}__{}__{}.pkl" \
                             .format(hash_, int(cache[hash_][0].timestamp()),
                                     int(cache[hash_][1].timestamp())))

        self._universe = ds_[(ds_.index >= self.start) & (ds_.index <= self.end)]

    def load_from_remote(self):
        print("loading data from web")
        dfs = pd.DataFrame()
        # For loop for grabing yahoo finance data and setting as a dataframe
        for stock in self.stocks:
            # Set DataFrame as the Stock Ticker
            df_ = DataReader(stock, 'yahoo', self.start, self.end)
            df_["symbol"] = stock
            dfs = pd.concat([dfs, df_], axis=0)

        self._universe = dfs

    def to_cache(self):
        cache = self.get_cache_info()
        hash_ = str(self._hash_tickers())

        if hash_ in cache:
            os.remove("cache__{}__{}__{}.pkl".format(hash_, int(cache[hash_][0].timestamp()),
                                                     int(cache[hash_][1].timestamp())))

        self._universe.to_pickle("cache__{}__{}__{}.pkl".format(self._hash_tickers(),
                                                                int(self.start.timestamp()),
                                                                int(self.end.timestamp())))

    def is_cached(self):
        cache = self._get_cache()
        hash_ = str(self._hash_tickers())
        return hash_ in cache and cache[hash_][0] <= self.start and cache[hash_][1] >= self.end

    def get_cache_info(self):
        """
        @rtype: dict {hash: (datetime_start,datetime_end)}
        """
        ret_dict = dict()
        cache_files = glob.glob('cache__*.pkl')
        for _ in cache_files:
            vals = _.split('__')
            ret_dict[(vals[1])] = (datetime.fromtimestamp(int(vals[2])),
                                   datetime.fromtimestamp(int(vals[3][:-4])))

        return ret_dict


