import unittest
from decent_parser import Evaluator


class TestEvaluator(unittest.TestCase):
    """
    unit test
    """

    def test_parse(self):
        """
        expect valid value
        """

        parser = Evaluator()
        value = parser.parse('2*2')
        self.assertEqual(value, 4)
