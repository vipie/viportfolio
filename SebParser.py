import numpy as np

from BaseParser import BaseParser
from utils import *
from datetime import datetime

import io

class SebParser(BaseParser):

    def __init__(self, file_loader):
        '''
        :param file_text: Path to mutual fund report file
        '''

        regex = r'(\w*).*SubFund LEI;(\w*).*Date;([\d-]*).*(ISIN;Security Name;.*)'
        m = re.match(regex, file_loader.load(), re.DOTALL)
        self.name = m.group(1)  # SEB_Russia_Fund
        self.date = datetime.strptime(m.group(3), '%Y-%m-%d')

        self.parsed_data = pd.read_csv(io.StringIO(m.group(4)), header=0, delimiter=';').dropna(how='all')
        self.parsed_data.rename(columns={'Security Name': 'Name',
                                         'PF Exposure Weight': 'Weight'}, inplace=True)

        self.parsed_data["Code"] = np.nan
        self.parsed_data.Weight = self.parsed_data.Weight.map(lambda x: float(x) * 100)
        self.parsed_data = self.parsed_data.sort_values(by='Weight', ascending=False)
        self.parsed_data = self.parsed_data.reset_index(drop=True)