import unittest
from MsciParser import MsciParser
import pandas as pd
from datetime import datetime
from SebParser import SebParser
from voya import VoyaParser
from loader import BaseLoader
from franklin import FranklinParser

class ParserTests():

    def test_parser_type(self):
        self.assertIsInstance(self.parser.parsed_data, pd.DataFrame)

    def test_parser_columns_len(self):
        self.assertGreaterEqual(len(self.parser.parsed_data.columns), 4)

    def test_parser_columns_contains_name(self):
        self.assertIn('Name', (self.parser.parsed_data.columns))

    def test_parser_columns_contains_weight(self):
        self.assertIn('Weight', (self.parser.parsed_data.columns))

    # def test_parser_columns_contains_country(self):
    #    self.assertIn('Country',(self.parser.parsed_data.columns))

    def test_parser_columns_contains_code(self):
        self.assertIn('Code', (self.parser.parsed_data.columns))

    def test_parser_date_type(self):
        self.assertIsInstance(self.parser.date, datetime)

    def test_parser_weight_sum(self):
        self.assertGreater(self.parser.parsed_data.Weight.sum(), 99)

    def test_parser_weight_sum2(self):
        self.assertLessEqual(self.parser.parsed_data.Weight.sum(), 100.1)

class MsciParserTestCase(unittest.TestCase, ParserTests):
    def setUp(self):
        self.parser = MsciParser(BaseLoader('https://app2.msci.com/eqb/custom_indexes/russia_performance.xls'))

class SebParserTestCase(unittest.TestCase, ParserTests):
        def setUp(self):
            self.parser = SebParser(BaseLoader('https://seb.se/pow/fmk/2500/csv/SEB_Russia_Fund_52990077SLDTU8UMXF91.csv'))

class VoyaParserTestCase(unittest.TestCase, ParserTests):
    def setUp(self):
        self.parser = VoyaParser(BaseLoader("https://individuals.voya.com/document/holdings/voya-russia-fund-monthly-holdings"
                                 "-xls.xls"))

class FranklinParserTestCase(unittest.TestCase, ParserTests):
    def setUp(self):
        self.parser = FranklinParser(BaseLoader("https://www.franklintempleton.com/investor/investments-and-solutions"
                                            "/investment-options/etfs/portfolio/26356/franklin-ftse-russia-etf/FLRU"
                                            "?gwbid=gw.portfolio"))

if __name__ == '__main__':
    unittest.main()
