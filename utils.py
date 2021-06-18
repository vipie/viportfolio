import json
# For time stamps
from datetime import datetime
#import cvxpy; cvxpy.installed_solvers()

import pandas as pd
import numpy as np
from scipy import stats
#import requests
import time
import glob
import os
from tabulate import tabulate

from pandas_datareader.data import DataReader
from datetime import datetime
from pypfopt.efficient_frontier import EfficientFrontier
from pypfopt import risk_models
from pypfopt import expected_returns
from pypfopt.discrete_allocation import DiscreteAllocation, get_latest_prices

from dateutil.relativedelta import relativedelta

class ConfigLoader:
    def __init__(self):
        with open('config.json') as f:
            self.config = json.load(f)

    @staticmethod
    def write_config_example():
        """
        Write config_example.json file for easy creation config.json
        :return:
        """
        ru_funds = {'seb' : {'description': 'SEB Russia Fund',
                             'url': 'http://seb.se/pow/fmk/2500/csv/SEB_Russia_Fund_52990077SLDTU8UMXF91.csv'},
                    'franklin': {'description': 'Franklin FTSE Russia ETF',
                                'url': 'https://www.franklintempleton.com/investor/investments-and-solutions/investment-options/etfs/portfolio/26356/franklin-ftse-russia-etf/FLRU?gwbid=gw.portfolio'},
                    'msci': {'description': 'MSCI Russia',
                    'url': 'https://app2.msci.com/eqb/custom_indexes/russia_performance.xls'}}
        ru_holdings = {'SBER.ME': 'Sberbank of Russia',
                       'GAZP.ME': 'Gazprom',
                       'SBERP.ME': 'Sberbank of Russia (Preferred)',
                       'LKOH.ME': 'Lukoil',
                       'GMKN.ME': 'MMC "NORILSK NICKEL',
                       'YNDX.ME': 'Yandex',
                        'NVTK.ME': 'Novatek',
                       'TATN.ME': 'TATNEFT',
                       'TATNP.ME': 'TATNEFT (Preferred)',
                       'ROSN.ME': 'Rosneft',
                       'SNGS.ME': 'Surgutneftegas',
                       'SNGSP.ME': 'Surgutneftegas (Preferred)',
                        'MGNT.ME': 'Magnit',
                       'FIVE.ME': 'X5 Retail Group N.V.',
                       'MTSS.ME': 'Mobile TeleSystems',
                       'POLY.ME': 'Polymetal International plc',
                       'ALRS.ME': 'Alrosa',
                       'CHMF.ME': 'Severstal',
                       'PLZL.ME': 'Polyus',
                       'IRAO.ME': 'Inter RAO',
                       'NLMK.ME': 'NLMK',
                       'VTBR.ME': 'VTB Bank',
                       'MOEX.ME': 'Moscow Exchange',
                       'PHOR.ME': 'PhosAgro',
                        'TRNFP.ME': 'Transneft (Preferred)',
                       'MAGN.ME': 'Magnitogorsk Iron & Steel Works',
                       'RTKM.ME': 'Rostelecom',
                       'RUAL.ME': 'Rusal',
                       'AFLT.ME': 'Aeroflot',
                       'PIKK.ME': 'PIK GROUP',
                       'HYDR.ME': 'RusHydro',
                       'FEES.ME': 'Federal Grid Company of Unified Energy System',
                       'AFKS.ME': 'Sistema',
                       'LSRG.ME': 'LSR Group',
                       'CBOM.ME': 'CREDIT BANK OF MOSCOW',
                       'UPRO.ME': 'Unipro',
                       'DSKY.ME': 'Detsky mir',
                       'RNFT.ME': 'RussNeft',
                       'LNTA.ME': 'Lenta',
                       'SFIN.ME': 'SAFMAR Financial investments',
                       'MVID.ME': 'M.video'}
        universe_dict = {'ru': {'description': 'Russian stocks', 'funds': ru_funds, 'holdings': ru_holdings}}

        data = {'provider': 'yahoo',
                'universe': universe_dict}

        with open('config.json', 'w') as f:
            json.dump(data, f, indent=4, sort_keys=True)


class LoadUniverse:
    """
    Load data from web or cache
    """

    def __init__(self, config, universe_code, period):

        self.stocks = config['universe'][universe_code]['holdings'].keys()

        # Set up End and Start times for data grab
        self.end = self._round_datetime(datetime.now())
        self.start = self.end - relativedelta(months=period)

        if self._is_cached():
            self._load_from_cache()
        else:
            self._load_from_web()
            self._cache_universe()

    def _load_from_web(self):
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
        return hash(' '.join(sorted(self.stocks))) % 2 ** 30 # TODO set seed

    @property
    def universe(self):
        return self._universe

    def _is_cached(self):
        cache = self._get_cache()
        hash_ = str(self._hash_tickers())
        return hash_ in cache and cache[hash_][0] <= self.start and cache[hash_][1] >= self.end

    def _load_from_cache(self):
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

class PortfolioCreater:

    def __init__(self, universe_df, type, target_ret, depo):
        df_u = universe_df
        self.depo = depo

        df_u = df_u.universe.pivot_table(
                                    index='Date',
                                    columns='symbol',
                                    values='Close',
                                    aggfunc='sum'
                                )

        # Calculate expected returns and sample covariance
        mu = expected_returns.mean_historical_return(df_u)
        S = risk_models.sample_cov(df_u)

        # Optimise the portfolio for maximal Sharpe ratio
        ef = EfficientFrontier(mu, S)  # Use regularization (gamma=1)

        weights = ef.max_sharpe()
        cleaned_weights = ef.clean_weights()

        # Allocate
        latest_prices = get_latest_prices(df_u)

        da = DiscreteAllocation(
            cleaned_weights,
            latest_prices,
            total_portfolio_value=depo
        )

        allocation = da.lp_portfolio()[0]

        # Put the stocks and the number of shares from the portfolio into a df
        symbol_list = []
        num_shares_list = []

        for symbol, num_shares in allocation.items():
            symbol_list.append(symbol)
            num_shares_list.append(num_shares)

        # Now that we have the stocks we want to buy we filter the df for those ones
        df_buy = universe_df.universe.loc[universe_df.universe['symbol'].isin(symbol_list)]

        # Filter for the period to get the closing price

        max_dates = (df_buy.reset_index().groupby('symbol')).Date.agg(maxDate='max')
        df_buy = df_buy.reset_index() \
            .apply(lambda row: {'Company': row.symbol, "Close": row.Close, 'Date': row.Date} \
            if row.Date == max_dates.loc[row.symbol, 'maxDate'] else None, axis=1)

        df_buy = pd.DataFrame(list(df_buy.dropna())).sort_values(by='Company')

        # Add in the qty that was allocated to each stock
        df_buy['Quantity'] = num_shares_list

        # Calculate the amount we own for each stock
        df_buy['Amount'] = df_buy['Close'] * df_buy['Quantity']
        df_buy = df_buy.loc[df_buy['Quantity'] != 0]
        df_buy['Percent'] = round(100*df_buy['Amount']/depo, 2)
        self.portfolio = df_buy.sort_values(by='Amount')

    def __str__(self):
        #print(self.portfolio.to_markdown())
        return tabulate(self.portfolio, headers='keys', tablefmt='grid') + \
               "\n\nTotal usage {}% of depo ({})".format(round(self.portfolio['Percent'].sum(), 1),
                                                        round(self.portfolio['Percent'].sum()/100 * self.depo, 2))




