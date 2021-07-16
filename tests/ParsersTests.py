import unittest
from MsciParser import MsciParser
import pandas as pd
from datetime import datetime
from SebParser import SebParser


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
        self.assertLessEqual(self.parser.parsed_data.Weight.sum(), 100)


class MsciParserTestCase(unittest.TestCase, ParserTests):
    def setUp(self):
        self.parser = MsciParser('https://app2.msci.com/eqb/custom_indexes/russia_performance.xls')

class SebParserTestCase(unittest.TestCase, ParserTests):
        def setUp(self):
            self.parser = SebParser('https://seb.se/pow/fmk/2500/csv/SEB_Russia_Fund_52990077SLDTU8UMXF91.csv')

if __name__ == '__main__':
    unittest.main()
