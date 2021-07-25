import io
from datetime import datetime

import numpy as np

from parsers.base_parser import BaseParser
from utils import *

class FranklinParser(BaseParser):

    def parse(self, file_loader):
        '''
        :param file_loader: instance of BaseLoader class
        '''

        regex = r';.*;Portfolio Holdings for ([\w\s]*) as of ([0-9/]{10}).*(SECURITY IDENTIFIER;ISIN;.*;)\"Important ' \
                r'Legal Information.* '

        m = re.match(regex, file_loader.load(), re.DOTALL)
        self.name = m.group(1)  # Voya Russia Fund
        self.date = datetime.strptime(m.group(2), '%m/%d/%Y')  # '07/22/2021

        self.parsed_data = pd.read_csv(io.StringIO(m.group(3)), header=0, delimiter=';').dropna(how='all')
        self.parsed_data.rename(columns={'SECURITY NAME': 'Name', 'WEIGHT (%)': 'Weight',
                                         'SECURITY IDENTIFIER': 'Code'},
                                inplace=True)
