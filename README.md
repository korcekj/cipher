# Cipher
A simple commandline app for encrypting and decrypting your files
# Installation

## Manual
```bash
  $ git clone https://github.com/korcekj/cipher.git
  $ cd cipher
  $ python setup.py install
```
# Usage
```bash
$ cipher
```
## Encryption
`-in <file_path>`
`-out <file_path>`
`-k <file_path>`
```bash
$ cipher e -in ./to_enc.txt
```
## Decryption
`-in <file_path>`
`-out <file_path>`
`-k <file_path>`
```bash
$ cipher d -in ./to_enc.txt.enc -k ./secret.key
```