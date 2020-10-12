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
$ cipher --help
```
## Encryption
* `-in <file_path> [required] - Cesta k súboru určeného na šifrovanie` 
* `-out <file_path> - Cesta k výstupnému súboru, výsledok šifrovania` 
* `-k <file_path> - Cesta k súboru kľúča, ak nie je poskytnutá, kľúč bude vygenerovaný vo výstupnej lokácii` 
```bash
$ cipher e -in your_dir/file.txt
```
## Decryption
* `-k <file_path> [required] - Cesta k súboru kľúča`
* `-in <file_path> [required] - Cesta k zašifrovanému súboru`
* `-out <file_path> - Cesta k vústupneému súboru, výsledok dešifrovania`
```bash
$ cipher d -in your_dir/file.txt.enc -k your_dir/secret.key
```