from BaseParser import BaseParser
from utils import *
from datetime import datetime

import requests, io

class SebParser(BaseParser):

    def __init__(self, file_path):
        '''
        :param file_path: Path to mutual fund report file
        in this method we handle all rows in DataFrame using chain of responsibility.
        You can similarly define your conditions as handler classes in heirs of BaseParser class.
        This method must create:
        - DataFrame with parsed data in self.parsed_data,
        - datetime of report in self.date
        - name of mutual fund in self.name
        IMPORTANT: condition in Handlers may intersect, but need to call next handler
        '''

        r = requests.get(file_path, allow_redirects=True)
        self.df = pd.read_csv(io.BytesIO(r.content), delimiter=';', header=None)

        # create of chain of responsibility

        self.handlers = self.HandleHeaderAndStartBody(
            self.HandleEndBody(
                self.HandleNameAndDate(
                    self.NullHandler())))

        self.start_index = self.end_index = self.columns = None

        for index, row in self.df.iterrows():
            self.handlers.handle(self, row, index)

    class NullHandler:
        '''
        Null hanhdler for chain of responsibility implementation
        '''

        def __init__(self, successor=None):
            self.__successor = successor

        def handle(self, parser, row, index):
            if self.__successor is not None:
                self.__successor.handle(parser, row, index)

    class HandleNameAndDate(NullHandler):
        '''
        Find and initialize date and name of mutual fund
        '''

        def handle(self, parser, row, index):
            if (row[0]) == 'SubFund LEI' and (index + 1) < parser.df.shape[0] and \
                    (parser.df.iloc[index + 1, 0]) == 'Date' and index > 0:
                parser.name = parser.df.iloc[index - 1, 0]
                parser.date = datetime.strptime(parser.df.iloc[index + 1, 1], '%Y-%m-%d')
            else:
                super().handle(parser, row, index)

    class HandleHeaderAndStartBody(NullHandler):
        '''
        Find and initialize header and start index of "body"
        '''

        def handle(self, parser, row, index):
            if (row[0]) == 'ISIN' and (row[1]) == 'Security Name':

                parser.start_index = (index + 1, 0)
                parser.columns = parser.df.iloc[index: index + 1, :].values.flatten().tolist()
                parser.columns[1] = 'Name'
                parser.columns[19] = 'Weight'
                parser.columns[0] = 'Code'
            else:
                super().handle(parser, row, index)

    class HandleEndBody(NullHandler):
        '''
        Find end index of "body"
        '''

        def handle(self, parser, row, index):
            if is_isin_code(row[0]) and index == parser.df.shape[0] - 1:
                parser.end_index = (index, 0)
                parser.parsed_data = parser.df.iloc[parser.start_index[0]:parser.end_index[0], :].dropna(how='all')
                parser.parsed_data.columns = parser.columns
                parser.parsed_data = parser.parsed_data.reset_index(drop=True)
                parser.parsed_data.Weight = parser.parsed_data.Weight.map(lambda x: float(x) * 100)
            else:
                super().handle(parser, row, index)