from tabulate import tabulate
from utils import *

class BaseParser:
    def __init__(self):
        raise NotImplementedError

    def pretty_print(self, deposit=None):
        print_df = self.parsed_data.loc[:, ['Name', 'Code', 'ISIN', 'Weight']]
        print(self.name + " assets on " + self.date.strftime("%Y-%m-%d"))

        if deposit is not None:
            print_df['Asset value'] = (deposit / 100) * print_df.Weight

        print_df = print_df.sort_values(by='Weight', ascending=False).dropna(axis='columns', how='all')
        print(tabulate(print_df, headers='keys', tablefmt='grid'))

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


