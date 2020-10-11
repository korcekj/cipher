# Cipher
A simple commandline app for encrypting and decrypting your files
# Installation

## Manual
```bash
  $ git clone 
  $ cd cipher
  $ python setup.py install
```
# Usage
```bash
$ cipher
```
## Encrypt
`-in <file_path>`
`-out <file_path>`
`-k <file_path>`
```bash
$ cipher e -in ./to_enc.txt
```
## Decrypt
`-in <file_path>`
`-out <file_path>`
`-k <file_path>`
```bash
$ cipher d -in ./to_enc.txt.enc -k ./secret.key
```