#!/usr/bin/env python3

import argparse


def fprint(text, variable):
    print(f'{text:>22} {variable}')


def left_rotate(block, n_shifts):
    return block[n_shifts:] + block[:n_shifts]


def permute(block, table):
    return ''.join(block[i] for i in table)


def gen_subkeys(key):
    key_permutation_table = [
        56, 48, 40, 32, 24, 16, 8,
        0, 57, 49, 41, 33, 25, 17,
        9, 1, 58, 50, 42, 34, 26,
        18, 10, 2, 59, 51, 43, 35,
        62, 54, 46, 38, 30, 22, 14,
        6, 61, 53, 45, 37, 29, 21,
        13, 5, 60, 52, 44, 36, 28,
        20, 12, 4, 27, 19, 11, 3
    ]
    compression_permutation_table = [
        13, 16, 10, 23, 0, 4,
        2, 27, 14, 5, 20, 9,
        22, 18, 11, 3, 25, 7,
        15, 6, 26, 19, 12, 1,
        40, 51, 30, 36, 46, 54,
        29, 39, 50, 44, 32, 47,
        43, 48, 38, 55, 33, 52,
        45, 41, 49, 35, 28, 31
    ]
    left_rotate_order = [1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1]
    key_permutation = permute(key, key_permutation_table)

    fprint('KEY:', key)
    fprint('KEY PERMUTATION', key_permutation)

    lk = key_permutation[:28]
    rk = key_permutation[28:]

    subkeys = []
    for n_shifts in left_rotate_order:
        lk = left_rotate(lk, n_shifts)
        rk = left_rotate(rk, n_shifts)
        compression_permutation = permute(lk + rk, compression_permutation_table)
        subkeys.append(compression_permutation)

    return subkeys


def xor(block_1, block_2):
    return bin(int(block_1, 2) ^ int(block_2, 2))[2:].zfill(len(block_1))


def s_box(block):
    s_box_table = [
        [
            [14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
            [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
            [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
            [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13]
        ],
        [
            [15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],
            [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],
            [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],
            [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9]
        ],
        [
            [10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8],
            [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1],
            [13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7],
            [1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12]
        ],
        [
            [7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15],
            [13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9],
            [10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4],
            [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14]
        ],
        [
            [2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],
            [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
            [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],
            [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3]
        ],
        [
            [12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],
            [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],
            [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6],
            [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13]
        ],
        [
            [4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],
            [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],
            [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],
            [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12]
        ],
        [
            [13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],
            [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],
            [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],
            [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11]
        ]
    ]
    output = ''

    for i in range(8):
        sub_str = block[i * 6:i * 6 + 6]
        row = int(sub_str[0] + sub_str[-1], 2)
        column = int(sub_str[1:5], 2)
        output += f'{s_box_table[i][row][column]:04b}'

    return output


def hex_to_bin(file):
    bin_table = ['0000', '0001', '0010', '0011',
                 '0100', '0101', '0110', '0111',
                 '1000', '1001', '1010', '1011',
                 '1100', '1101', '1110', '1111'
                 ]

    return ''.join(bin_table[int(hex_digit, 16)] for hex_digit in file.read()[:-1])


def pad(bin_str):
    return bin_str + '0' * ((64 - len(bin_str) % 64) % 64)


def round(input_block, subkey):
    expansion_permutation_table = [
        31, 0, 1, 2, 3, 4,
        3, 4, 5, 6, 7, 8,
        7, 8, 9, 10, 11, 12,
        11, 12, 13, 14, 15, 16,
        15, 16, 17, 18, 19, 20,
        19, 20, 21, 22, 23, 24,
        23, 24, 25, 26, 27, 28,
        27, 28, 29, 30, 31, 0
    ]
    p_box_table = [
        15, 6, 19, 20, 28, 11, 27, 16,
        0, 14, 22, 25, 4, 17, 30, 9,
        1, 7, 23, 13, 31, 26, 2, 8,
        18, 12, 29, 5, 21, 10, 3, 24
    ]
    l = input_block[:32]
    r = input_block[32:]
    expansion_permutation = permute(r, expansion_permutation_table)
    xor1 = xor(expansion_permutation, subkey)
    s_box_output = s_box(xor1)
    p_box = permute(s_box_output, p_box_table)
    xor2 = xor(p_box, l)
    output = r + xor2

    fprint('INPUT:', f'{l} {r}')
    fprint('SUBKEY:', subkey)
    fprint('EXPANSION PERMUTATION:', expansion_permutation)
    fprint('XOR:', xor1)
    fprint('S-BOX SUBSTITUTION:', s_box_output)
    fprint('P-BOX PERMUTATION:', p_box)
    fprint('XOR:', xor2)
    fprint('SWAP:', f'{r} {xor2}')
    fprint('OUTPUT:', output)

    return output


def des(input_block, subkeys, crypt_type):
    initial_permutation_table = [
        57, 49, 41, 33, 25, 17, 9, 1,
        59, 51, 43, 35, 27, 19, 11, 3,
        61, 53, 45, 37, 29, 21, 13, 5,
        63, 55, 47, 39, 31, 23, 15, 7,
        56, 48, 40, 32, 24, 16, 8, 0,
        58, 50, 42, 34, 26, 18, 10, 2,
        60, 52, 44, 36, 28, 20, 12, 4,
        62, 54, 46, 38, 30, 22, 14, 6
    ]
    final_permutation_table = [
        39, 7, 47, 15, 55, 23, 63, 31,
        38, 6, 46, 14, 54, 22, 62, 30,
        37, 5, 45, 13, 53, 21, 61, 29,
        36, 4, 44, 12, 52, 20, 60, 28,
        35, 3, 43, 11, 51, 19, 59, 27,
        34, 2, 42, 10, 50, 18, 58, 26,
        33, 1, 41, 9, 49, 17, 57, 25,
        32, 0, 40, 8, 48, 16, 56, 24
    ]
    initial_permutation = permute(input_block, initial_permutation_table)

    print()
    print()
    fprint('BLOCK:', input_block)
    fprint('INITIAL PERMUTATION:', initial_permutation)

    if crypt_type == 'e':
        start = 0
        end = 16
        step = 1
    else:
        start = 15
        end = -1
        step = -1

    output = initial_permutation
    for i, j in enumerate(range(start, end, step), 1):
        print()
        print(f'ROUND {i}:')
        output = round(output, subkeys[j])

    swap = output[32:] + output[:32]
    final_permutation = permute(swap, final_permutation_table)

    print()
    fprint('SWAP:', swap)
    fprint('FINAL PERMUTATION:', final_permutation)

    return final_permutation


def crypt(mode, crypt_type, key_file, infile, outfile, iv_file=None):
    bin_in_str = pad(hex_to_bin(infile))
    subkeys = gen_subkeys(hex_to_bin(key_file))
    bin_out_str = ''

    if mode == 'ecb':
        for i in range(0, len(bin_in_str), 64):
            bin_out_str += des(bin_in_str[i:i + 64], subkeys, crypt_type)
    else:
        last_block = hex_to_bin(iv_file)

        for i in range(0, len(bin_in_str), 64):
            block = bin_in_str[i:i + 64]

            if crypt_type == 'e':
                block = xor(block, last_block)

            output = des(block, subkeys, crypt_type)

            if crypt_type == 'e':
                last_block = output
            else:
                output = xor(output, last_block)
                last_block = block

            bin_out_str += output

    outfile.write(f'{int(bin_out_str, 2):0{len(bin_out_str) // 4}X}\n')


if __name__ == "__main__":
    def add_common_arguments(parser):
        crypt_group = parser.add_mutually_exclusive_group(required='True')
        crypt_group.add_argument('-e', action='store_const', dest='option', const='e', help='encrypt')
        crypt_group.add_argument('-d', action='store_const', dest='option', const='d', help='decrypt')
        parser.add_argument('key_file', type=argparse.FileType('r'),
                            help='text file to be used as key for encryption/decryption')
        parser.add_argument('infile', type=argparse.FileType('r'),
                            help='text file to be used as input for encryption/decryption')
        parser.add_argument('outfile', type=argparse.FileType('w'),
                            help='text file to be used as output for encryption/decryption')

        return parser


    parser = argparse.ArgumentParser()
    sub_parsers = parser.add_subparsers(dest='mode')
    ecb_parser = add_common_arguments(
        sub_parsers.add_parser('ecb', help='use Electronic Codebook (ECB) encryption mode'))
    cbc_parser = add_common_arguments(
        sub_parsers.add_parser('cbc', help='use Cipher Block Chaining (CBC) encryption mode'))
    cbc_parser.add_argument('iv_file', type=argparse.FileType('r'),
                            help='text file to be used as IV for encryption/decryption')
    args = parser.parse_args()

    if args.mode == 'ecb':
        crypt(args.mode, args.option, args.key_file, args.infile, args.outfile)
    else:
        crypt(args.mode, args.option, args.key_file, args.infile, args.outfile, args.iv_file)
