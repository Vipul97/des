# Data Encryption Standard (DES)

This repository contains an implementation of the Data Encryption Standard (DES) in Python 3.12. It supports two modes of
operation: Electronic Codebook (ECB) and Cipher Block Chaining (CBC).

## Features

- **Modes Supported**:
    - **Electronic Codebook (ECB)**: Simple mode where plaintext is divided into blocks and each block is encrypted
      independently.
    - **Cipher Block Chaining (CBC)**: Each block of plaintext is XORed with the previous ciphertext block before being
      encrypted, enhancing security.

## Getting Started

To run the program, execute `des.py` with the desired mode and necessary parameters.

### Usage

        usage: des.py [-h] {ecb,cbc} ...

        positional arguments:
          {ecb,cbc}
            ecb       Use Electronic Codebook (ECB) encryption mode.
            cbc       Use Cipher Block Chaining (CBC) encryption mode.
        
        optional arguments:
          -h, --help  show this help message and exit

#### Mode-Specific Usage

##### ECB Mode

        usage: des.py ecb [-h] (-e | -d) key_file infile outfile
        
        positional arguments:
          key_file    Path to the text file used as the key for encryption/decryption.
          infile      Path to the text file used as input for encryption/decryption.
          outfile     Path to the text file where the output will be written.
        
        optional arguments:
          -h, --help  show this help message and exit
          -e          Encrypt the input file.
          -d          Decrypt the input file.

##### CBC Mode

        usage: des.py cbc [-h] (-e | -d) key_file infile outfile iv_file
        
        positional arguments:
          key_file    Path to the text file used as the key for encryption/decryption.
          infile      Path to the text file used as input for encryption/decryption.
          outfile     Path to the text file where the output will be written.
          iv_file     Path to the text file used as IV for encryption/decryption.
        
        optional arguments:
          -h, --help  show this help message and exit
          -e          Encrypt the input file.
          -d          Decrypt the input file.

## Examples

### Encrypting a Text File Using ECB Mode

```commandline
python des.py ecb -e key.txt input.txt output.txt
```

### Decrypting a Text File Using CBC Mode

```commandline
python des.py cbc -d key.txt input.txt output.txt iv.txt
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.