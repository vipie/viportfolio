from tabulate import tabulate
from utils import *

class AbstractParser:
    def __init__(self):
        raise NotImplementedError

    def pretty_print(self, deposit=None):
        print_df = self.parsed_data.loc[:, ['Name', 'Code', 'Weight']]

        if deposit is not None:
            print_df['Deposit'] = (deposit / 100) * print_df.Weight

        print(tabulate(print_df, headers='keys', tablefmt='psql'))

    def compare(self, parser):
        raise NotImplementedError

    def get_info(self, isin_or_ticker):

        if is_isin_code(isin_or_ticker):
            return self.get_info_by_isin()

        return self.get_info_by_ticker()

    def get_info_by_ticker(self):
        raise NotImplementedError

    def get_info_by_isin(self):
        raise NotImplementedError


