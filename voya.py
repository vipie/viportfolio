import io
from datetime import datetime

import numpy as np

from BaseParser import BaseParser
from utils import *

class VoyaParser(BaseParser):

    def __init__(self, file_loader):
        '''
        :param file_loader: instance of BaseLoader class
        '''

        regex = r';([\w\s]*).*Portfolio Holdings as of (.* 20..).*;(Ticker;Security Name;.*)("Important Legal ' \
                r'Information.*) '

        m = re.match(regex, file_loader.load(), re.DOTALL)
        self.name = m.group(1)  # Voya Russia Fund
        self.date = datetime.strptime(m.group(2), '%B %d, %Y')  # June 30, 2021

        self.parsed_data = pd.read_csv(io.StringIO(m.group(3)), header=0, delimiter=';').dropna(how='all')
        self.parsed_data.rename(columns={'Security Name': 'Name', 'Crncy': 'Currency', 'Ticker': 'Code'},
                                inplace=True)

        self.parsed_data["ISIN"] = np.nan
        self.parsed_data["Weight"] = self.parsed_data['Market Value'] * 100 / (self.parsed_data['Market Value'].sum())
        self.parsed_data = self.parsed_data.sort_values(by='Weight', ascending=False)
        self.parsed_data = self.parsed_data.reset_index(drop=True)
