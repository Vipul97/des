# Data Encryption Standard (DES)
Implementation of Data Encryption Standard (DES) in Python 3.8.

Supports Electronic Codebook (ECB) and Cipher Block Chaining (CBC) Block Cipher Modes of Operation.

## Instructions
1. Input the hexadecimal input in `des/plaintext.txt` (for Encryption) or `des/ciphertext.txt` (for Decryption).
2. Input the hexadecimal key in `des/key.txt`.
3. If using the CBC Block Cipher Mode of Operation, input the hexadecimal Initialization Vector (IV) in `des/iv.txt`.
4. Run `des.py`.

        usage: des.py [-h] (-e | -d) [-ecb | -cbc]

5. Hexadecimal output will be saved in `des/ciphertext.txt` (if Encryption option is used) or `des/plaintext.txt` (if Decryption option is used).

