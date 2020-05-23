import unittest
from string_parser import StringParser


class TestStringParser(unittest.TestCase):
    def test_str_true(self):
        parser = StringParser()
        test_string = '{a=c>b}'
        result = parser.check_string(test_string)
        self.assertEqual(result, True)

    def test_str_couple_true(self):
        parser = StringParser()
        test_string = '{a=b>c;d=c<d}'
        result = parser.check_string(test_string)
        self.assertEqual(result, True)

    def test_str_complex_true(self):
        parser = StringParser()
        test_string = '{a=b*b+3>c-d;d=5+a<4-d}'
        result = parser.check_string(test_string)
        self.assertEqual(result, True)

    def test_str_missing_false(self):
        parser = StringParser()
        test_string = '{a=2'
        result = parser.check_string(test_string)
        self.assertEqual(result, False)

    def test_str_excess_false(self):
        parser = StringParser()
        test_string = '{a=2}}'
        result = parser.check_string(test_string)
        self.assertEqual(result, False)

    def test_str_false(self):
        parser = StringParser()
        test_string = '{a>b}'
        result = parser.check_string(test_string)
        self.assertEqual(result, False)
