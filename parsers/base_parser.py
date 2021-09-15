from tabulate import tabulate
from utils import *

class BaseParser:
    def __init__(self, file_loader, aliases):
        self.parse(file_loader)
        self.aliases = aliases
        self.parsed_data = self.parsed_data.sort_values(by='Weight', ascending=False)
        self.parsed_data = self.parsed_data.reset_index(drop=True)

    def pretty_print(self, deposit=None):
        print_df = self.parsed_data.loc[:, ['Name', 'Code', 'ISIN', 'Weight']]
        print(self.name + " assets on " + self.date.strftime("%Y-%m-%d"))

        if deposit is not None:
            print_df['Asset value'] = (deposit / 100) * print_df.Weight

        print_df = print_df.sort_values(by='Weight', ascending=False).dropna(axis='columns', how='all')
        print(tabulate(print_df, headers='keys', tablefmt='grid'))

    def print_db_report(self, deposit=None):
        print_df = self.parsed_data.loc[:, ['Name', 'Code', 'ISIN', 'Weight']]
        print(self.name + " assets on " + self.date.strftime("%Y-%m-%d"))

        if deposit is not None:
            print_df['Asset value'] = (deposit / 100) * print_df.Weight

        print_df = print_df.sort_values(by='Weight', ascending=False).dropna(axis='columns', how='all')
        print_df["Normal_Form"] = None

        for index, row in print_df.iterrows():
            print_df.at[index, 'Normal_Form'] = self.aliases.get(row["Name"], None)


        print(tabulate((print_df[print_df['Normal_Form'].notnull()]), headers='keys', tablefmt='grid'))

        print("Unknown names:")
        print(list((print_df[print_df['Normal_Form'].isnull()])["Name"]))


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

    def parse(self, file_loader):
        raise NotImplementedError




