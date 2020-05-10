# Data Encryption Standard (DES)
Implementation of Data Encryption Standard (DES) in Python 3.8.

Supports Electronic Codebook (ECB) and Cipher Block Chaining (CBC) Block Cipher Modes of Operation.

## Instructions
Run `des.py`.

        usage: des.py [-h] {ecb,cbc} ...

        positional arguments:
          {ecb,cbc}
            ecb       use Electronic Codebook (ECB) encryption mode
            cbc       use Cipher Block Chaining (CBC) encryption mode
        
        optional arguments:
          -h, --help  show this help message and exit
<!-- -->
        usage: des.py ecb [-h] (-e | -d) key_file infile outfile
        
        positional arguments:
          key_file    text file to be used as key for encryption/decryption
          infile      text file to be used as input for encryption/decryption
          outfile     text file to be used as output for encryption/decryption
        
        optional arguments:
          -h, --help  show this help message and exit
          -e          encrypt
          -d          decrypt
<!-- -->
        usage: des.py cbc [-h] (-e | -d) key_file infile outfile iv_file
        
        positional arguments:
          key_file    text file to be used as key for encryption/decryption
          infile      text file to be used as input for encryption/decryption
          outfile     text file to be used as output for encryption/decryption
          iv_file     text file to be used as IV for encryption/decryption
        
        optional arguments:
          -h, --help  show this help message and exit
          -e          encrypt
          -d          decrypt
