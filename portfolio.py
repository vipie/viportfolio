from pypfopt.efficient_frontier import EfficientFrontier
from pypfopt import risk_models
from pypfopt import expected_returns
from pypfopt.discrete_allocation import DiscreteAllocation, get_latest_prices
from utils import r_

import pandas as pd

from tabulate import tabulate

class Portfolio:

    def __init__(self, universe_instance, type, target_ret, depo):
        self.universe = universe_instance.universe
        self.depo = depo
        self.type = type
        self.target_ret =  target_ret
        self.__create_portfolio()

    def __create_portfolio(self):
        df_u = self.universe.pivot_table(
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

        #ef.add_objective(objective_functions.L2_reg, gamma=1)

        optimizer = {
            'optimal': (ef.efficient_return, True),
            'maxsharpe': (ef.max_sharpe, False),
        }

        weights = optimizer[self.type][0](self.target_ret) if optimizer[self.type][1] else optimizer[self.type][0]()

        cleaned_weights = ef.clean_weights()

        # Allocate
        latest_prices = get_latest_prices(df_u)
        da = DiscreteAllocation(
            cleaned_weights,
            latest_prices,
            total_portfolio_value=self.depo
        )
        allocation = da.lp_portfolio()[0]

        # Put the stocks and the number of shares from the portfolio into a df
        symbol_list = []
        num_shares_list = []
        for symbol, num_shares in allocation.items():
            symbol_list.append(symbol)
            num_shares_list.append(num_shares)

        # Now that we have the stocks we want to buy we filter the df for those ones
        df_buy = self.universe.loc[self.universe['symbol'].isin(symbol_list)]

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
        df_buy['Percent'] = r_(100 * df_buy['Amount'] / self.depo)
        self.portfolio = df_buy.sort_values(by='Amount')
        self.portfolio_verbose = ef.portfolio_performance(verbose=True)

    def __str__(self):
        return tabulate(self.portfolio, headers='keys', tablefmt='grid') + \
               "\n\nTotal usage {}% of depo ({}). \n expected return: {}, volatility: {}, Sharpe ratio: {} ". \
                   format(r_(self.portfolio['Percent'].sum()),
                          r_(self.portfolio['Percent'].sum()/100 * self.depo),
                          r_(self.portfolio_verbose[0]), r_(self.portfolio_verbose[1]),
                          r_(self.portfolio_verbose[2])
                          )