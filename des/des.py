#!/usr/bin/env python3

import argparse


def left_rotate(l, n_shifts):
    return l[n_shifts:] + l[:n_shifts]


def permute(input, table):
    return ''.join(input[i] for i in table)


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

    print(f'{"KEY:":>22} {key}')
    print(f'{"KEY PERMUTATION:":>22} {key_permutation}')

    Lk = key_permutation[:28]
    Rk = key_permutation[28:]

    subkeys = []
    for n_shifts in left_rotate_order:
        Lk = left_rotate(Lk, n_shifts)
        Rk = left_rotate(Rk, n_shifts)
        compression_permutation = permute(Lk + Rk, compression_permutation_table)
        subkeys.append(compression_permutation)

    return subkeys


def xor(A, B):
    return bin(int(A, 2) ^ int(B, 2))[2:].zfill(len(A))


def s_box(input):
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
        sub_str = input[i * 6:i * 6 + 6]
        row = int(sub_str[0] + sub_str[-1], 2)
        column = int(sub_str[1:5], 2)
        output += f'{s_box_table[i][row][column]:04b}'

    return output


def read(filename):
    bin = ['0000', '0001', '0010', '0011',
           '0100', '0101', '0110', '0111',
           '1000', '1001', '1010', '1011',
           '1100', '1101', '1110', '1111'
           ]

    with open(f'{filename}.txt') as file:
        return ''.join(bin[int(hex, 16)] for hex in file.read()[:-1])


def pad(bin_str):
    return bin_str + '0' * ((64 - len(bin_str) % 64) % 64)


def round(input, subkey):
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
    L = input[:32]
    R = input[32:]
    expansion_permutation = permute(R, expansion_permutation_table)
    XOR1 = xor(expansion_permutation, subkey)
    s_box_output = s_box(XOR1)
    p_box = permute(s_box_output, p_box_table)
    XOR2 = xor(p_box, L)
    output = R + XOR2

    print(f'{"INPUT:":>22} {L} {R}')
    print(f'{"SUBKEY:":>22} {subkey}')
    print(f'{"EXPANSION PERMUTATION:":>22} {expansion_permutation}')
    print(f'{"XOR:":>22} {XOR1}')
    print(f'{"S-BOX SUBSTITUTION:":>22} {s_box_output}')
    print(f'{"P-BOX PERMUTATION:":>22} {p_box}')
    print(f'{"XOR:":>22} {XOR2}')
    print(f'{"SWAP:":>22} {R} {XOR2}')
    print(f'{"OUTPUT:":>22} {output}')

    return output


def DES(input, subkeys, crypt_type):
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
    initial_permutation = permute(input, initial_permutation_table)

    print()
    print()
    print(f'{"BLOCK:":>22} {input}')
    print(f'{"INITIAL PERMUTATION:":>22} {initial_permutation}')

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
    print(f'{"SWAP:":>22} {swap}')
    print(f'{"FINAL PERMUTATION:":>22} {final_permutation}')

    return final_permutation


def crypt(mode, crypt_type):
    if crypt_type == 'e':
        bin_in_str = pad(read('plaintext'))
        out_filename = 'ciphertext.txt'
    else:
        bin_in_str = pad(read('ciphertext'))
        out_filename = 'plaintext.txt'

    subkeys = gen_subkeys(read('key'))
    bin_out_str = ''

    if mode == 'ecb':
        for i in range(0, len(bin_in_str), 64):
            bin_out_str += DES(bin_in_str[i:i + 64], subkeys, crypt_type)
    else:
        IV = read('iv')
        toXOR = IV

        for i in range(0, len(bin_in_str), 64):
            block = bin_in_str[i:i + 64]

            if crypt_type == 'e':
                block = xor(block, toXOR)

            final_permutation = DES(block, subkeys, crypt_type)

            if crypt_type == 'e':
                output = final_permutation
                toXOR = final_permutation
            else:
                output = xor(final_permutation, toXOR)
                toXOR = block

            bin_out_str += output

    with open(out_filename, 'w') as out_str:
        out_str.write(f'{int(bin_out_str, 2):0{len(bin_out_str) // 4}X}\n')


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    crypt_group = parser.add_mutually_exclusive_group(required='True')
    crypt_group.add_argument('-e', action='store_const', dest='option', const='e')
    crypt_group.add_argument('-d', action='store_const', dest='option', const='d')
    mode_group = parser.add_mutually_exclusive_group()
    mode_group.add_argument('-ecb', action='store_const', dest='mode', const='ecb')
    mode_group.add_argument('-cbc', action='store_const', dest='mode', const='cbc')
    parser.set_defaults(mode='ecb')
    args = parser.parse_args()
    crypt(args.mode, args.option)