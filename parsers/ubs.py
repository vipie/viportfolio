import io
from datetime import datetime

import numpy as np

from parsers.base_parser import BaseParser
from utils import *

class UbsParser(BaseParser):

    def parse(self, file_loader):
        '''
        :param file_loader: instance of BaseLoader class
        '''

        regex = r'.*Data as at end-([\w]* \d{4})\n\n([\s\w-]*)\n\nFund Fact Sheet.*' \
                r'10 largest equity positions \(%\)\n(.*)\nFund\n([\d.\n]*)\nBenefits\n.*'


        m = re.match(regex, file_loader.load(), re.DOTALL)
        self.name = m.group(2)  # UBS Equity Russia P-acc
        self.date = datetime.strptime(m.group(1), '%B %Y')  # June 2021

        data = pd.DataFrame(list(zip(list(filter(None, m.group(3).split('\n'))),
                                     list(filter(None, m.group(4).split('\n'))))))

        data['Weight'] = data[1].astype(float)
        data.rename(columns={0: 'Name'}, inplace=True)
        self.parsed_data = data.drop(data.columns[[1]], axis=1)

        self.parsed_data["ISIN"] = np.nan
        self.parsed_data["Code"] = np.nan
