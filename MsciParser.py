from BaseParser import BaseParser
from utils import *
from datetime import datetime
import io
import numpy as np


import math

class MsciParser(BaseParser):

    def __init__(self, file_loader):
        '''
        :param file_loader: instance of BaseLoader class
        '''

        regex = r';([\w\s]*);.*;Closing Index Information as of \w*, (\w* \d{1,2}, \d{4});.*;' \
                r'(MSCI Code;Security Name;Price;.*);Sector Weights for.*'

        m = re.match(regex, file_loader.load(), re.DOTALL)
        self.name = m.group(1)  # MSCI Russia
        self.date = datetime.strptime(m.group(2), '%B %d, %Y')  # June 30, 2021

        self.parsed_data = pd.read_csv(io.StringIO(m.group(3)), header=0, delimiter=';').dropna(how='all')
        self.parsed_data.rename(columns={'Security Name': 'Name',
                                         'Weight%': 'Weight', 'Reuters Code (RIC)': 'Code'},
                                inplace=True)

        self.parsed_data["ISIN"] = np.nan
        self.parsed_data = self.parsed_data.sort_values(by='Weight', ascending=False)
        self.parsed_data = self.parsed_data.reset_index(drop=True)
