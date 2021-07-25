import pandas as pd
import glob
import os
from utils import *


from pandas_datareader.data import DataReader
from datetime import datetime


from dateutil.relativedelta import relativedelta

class Universe:
    """
    Create universe
    """

    def __init__(self, stocks, period):

        self.stocks = stocks

        # Set up End and Start times for data grab
        self.end = self._round_datetime(datetime.now())
        self.start = self.end - relativedelta(months=period)

        if self._is_cached():
            self._load_from_cache()
        else:
            self._load_from_web()
            self._cache_universe()

    def _load_from_web(self):
        print("loading data from web")
        dfs = pd.DataFrame()
        # For loop for grabing yahoo finance data and setting as a dataframe
        for stock in self.stocks:
            # Set DataFrame as the Stock Ticker
            df_ = DataReader(stock, 'yahoo', self.start, self.end)
            df_["symbol"] = stock
            dfs = pd.concat([dfs, df_], axis=0)

        self._universe = dfs

    def _round_datetime(self, dtme):
        return datetime(dtme.year, dtme.month, dtme.day)

    def _cache_universe(self):
        cache = self._get_cache()
        hash_ = str(self._hash_tickers())

        if hash_ in cache:
            os.remove("cache__{}__{}__{}.pkl".format(hash_, int(cache[hash_][0].timestamp()),
                                                     int(cache[hash_][1].timestamp())))

        self._universe.to_pickle("cache__{}__{}__{}.pkl".format(self._hash_tickers(),
                                                                int(self.start.timestamp()),
                                                                int(self.end.timestamp())))

    def _hash_tickers(self):
        return fast_hash(' '.join(sorted(self.stocks)), 'dsb8jk21ijdidwdhjhj')

    @property
    def universe(self):
        return self._universe

    def _is_cached(self):
        cache = self._get_cache()
        hash_ = str(self._hash_tickers())
        return hash_ in cache and cache[hash_][0] <= self.start and cache[hash_][1] >= self.end

    def _load_from_cache(self):
        print("loading data from cache")
        cache = self._get_cache()
        hash_ = str(self._hash_tickers())
        ds_ = pd.read_pickle("cache__{}__{}__{}.pkl".format(hash_,
                                                            int(cache[hash_][0].timestamp()),
                                                            int(cache[hash_][1].timestamp())))

        self._universe = ds_[(ds_.index >= self.start) & (ds_.index <= self.end)]

    def _get_cache(self):
        """
        @rtype: dict {hash: (datetime_start,datetime_end)}
        """
        ret_dict = dict()
        cache_files = glob.glob('cache__*.pkl')
        for _ in cache_files:
            vals = _.split('__')
            ret_dict[(vals[1])] = (datetime.fromtimestamp(int(vals[2])), datetime.fromtimestamp(int(vals[3][:-4])))

        return ret_dict