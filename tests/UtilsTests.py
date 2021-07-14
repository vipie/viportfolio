import unittest
import utils

class UtilsTestCase(unittest.TestCase):

    def test_is_isin_code0(self):
        self.assertEqual(utils.is_isin_code('U8213512781'), False)

    def test_is_isin_code1(self):
        self.assertEqual(utils.is_isin_code('US1234567890'), True)

    def test_is_isin_code2(self):
        self.assertEqual(utils.is_isin_code('US12345678904234'), False)

    def test_is_isin_code3(self):
        self.assertEqual(utils.is_isin_code('US12345_7890'), False)

    def test_is_isin_code4(self):
        self.assertEqual(utils.is_isin_code('USAB34507890'), True)

    def test_is_isin_code5(self):
        self.assertEqual(utils.is_isin_code(3464645), False)

    def test_is_isin_code6(self):
        self.assertEqual(utils.is_isin_code(None), False)

    def test_is_isin_code7(self):
        self.assertEqual(utils.is_isin_code('USABCDERTYKL'), False)

    def test_is_isin_code8(self):
        self.assertEqual(utils.is_isin_code('USABCDERTYK9'), True)



if __name__ == '__main__':
    unittest.main()
