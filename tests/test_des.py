import itertools
import unittest

from des.des import hex_to_bin, pad, left_rotate, permute, gen_subkeys, xor, s_box, round, des, crypt


class TestDES(unittest.TestCase):
    def test_hex_to_bin(self):
        self.assertEqual(hex_to_bin('0123456789ABCDEF'),
                         '0000000100100011010001010110011110001001101010111100110111101111')

    def test_pad(self):
        test_cases = [
            ('', 0),
            ('0', 64),
            ('0' * 32, 64),
            ('0' * 128, 128)
        ]
        for input_data, expected_length in test_cases:
            with self.subTest(input=input_data):
                self.assertEqual(len(pad(input_data)), expected_length)

    def test_left_rotate(self):
        self.assertEqual(left_rotate(['01' * 14], 1), ['10' * 14])

    def test_permute(self):
        self.assertEqual(permute('01' * 16, list(range(31, -1, -1))), '10' * 16)

    def test_gen_subkeys(self):
        expected_keys = [
            '101100001001001011001010110101010000001001010100',
            '101100000001101011010010110100011000001001010100',
            '001101000111101001010000010100011010011010001100',
            '000001100111010101010100001110000011010010001101',
            '010011100100010101010101001010100111000010100111',
            '010011111100000100101001001001100110100110100011',
            '100010111000000110101011101001100000100101010011',
            '101110010000101010001011110001111000001101010010',
            '001110010001101010001010110001011000001101001010',
            '001100000011100011001100010101001001011001001100',
            '000100000110110001010100010110001001010011101100',
            '010001000110110100110100000010001111110010101001',
            '110001101010010100100101001010100111110000110001',
            '110010111000011000100011101010110100100100110010',
            '111010011001001010101010100001010100101100010010',
            '101000011001001010101010100101010000101101010000'
        ]
        self.assertEqual(gen_subkeys('01' * 32), expected_keys)

    def test_xor(self):
        self.assertEqual(xor('01' * 24, '01' * 24), '0' * 48)

    def test_s_box(self):
        self.assertEqual(s_box('01' * 24), '11000001010100101111110101010110')

    def test_round(self):
        self.assertEqual(round('01' * 32, '01' * 24),
                         '0101010101010101010101010101010101101101100011101010110010011110')

    def test_des(self):
        expected_results = [
            '0011111110111110101011100011110101101101001101110111011011001100',
            '0011111110111110101011100011110101101101001101110111011011001100'
        ]

        for i, option in enumerate(['e', 'd']):
            self.assertEqual(des('01' * 32, ['01' * 24] * 16, option), expected_results[i])

    def test_crypt(self):
        expected_results = [
            'DA02CE3A89ECAC3BDA02CE3A89ECAC3B',
            '411B8280950607EF411B8280950607EF',
            'E7BE36D4719EB0B790DF1619A4B7FAB9',
            'BEE47D7F6AF9F810435D084E79AE63CF'
        ]

        for i, (mode, option) in enumerate(itertools.product(['ecb', 'cbc'], ['e', 'd'])):
            with self.subTest(mode=mode, option=option):
                with open('tests/test_key_file.txt') as test_key_file, \
                        open('tests/test_infile.txt') as test_infile, \
                        open('tests/test_outfile.txt', 'w+') as test_outfile:

                    if mode == 'cbc':
                        with open('tests/test_iv_file.txt') as test_iv_file:
                            crypt(mode, option, test_key_file, test_infile, test_outfile, test_iv_file)
                    else:
                        crypt(mode, option, test_key_file, test_infile, test_outfile)

                    test_outfile.seek(0)
                    self.assertEqual(test_outfile.read().strip(), expected_results[i])


if __name__ == '__main__':
    unittest.main()
