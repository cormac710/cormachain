from unittest import TestCase

from util.hex_binary_converter import convert_hex_to_binary

class TestHexToBinary(TestCase):
    def test_hex_to_binary(self):
        original_number = 789
        hex_number = hex(original_number)[2:]
        binary_number = convert_hex_to_binary(hex_number)
        print('test')
        self.assertTrue(int(binary_number, 2) == original_number)
