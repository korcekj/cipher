import os
import struct

from Crypto.Cipher import AES
from Crypto import Random


class CypherException(Exception):
    def __init__(self, message):
        # Call the base class constructor with the parameters it needs
        super().__init__(message)


def gen_key(key_dir, key_size=AES.block_size):
    key = Random.get_random_bytes(key_size)  # 128 bits key
    write_file(join_to_path(key_dir, 'secret.key'), key)
    return key


def get_key(key_file, key_size=AES.block_size):
    key = read_file(key_file, key_size)
    if len(key) < key_size:
        raise CypherException(f"Incorrect key length ({len(key)})")
    return key


def gen_iv(iv_size=AES.block_size):
    return Random.get_random_bytes(iv_size)  # 128 bits iv


def is_file(file):
    if not file:
        return False
    return os.path.isfile(file)


def get_dir(file):
    if not file:
        return None
    return os.path.dirname(file)


def get_abs_path(path):
    if not path:
        return None
    return os.path.abspath(path)


def get_basename(path):
    if not path:
        return None
    return os.path.basename(path)


def get_file_size(file):
    if not file:
        return None
    return os.path.getsize(file)


def join_to_path(directory, file_name):
    if not directory or not file_name:
        return None
    return os.path.join(directory, file_name)


def read_file(file, num_bytes=None, mode='rb'):
    if not is_file(file):
        raise CypherException("Provided file does not exists")

    with open(file, mode) as f:
        plaintext = f.read() if not num_bytes else f.read(num_bytes)
    return plaintext


def write_file(file, data, mode='wb'):
    with open(file, mode) as f:
        f.write(data)


def encrypt_file(key_path, in_file, out_file=None, chunk_size=64 * 1024):
    if not out_file:
        out_file = in_file + '.enc'
    if not key_path:
        key = gen_key(get_dir(out_file))
    else:
        key = get_key(key_path)

    iv = gen_iv()
    encryptor = AES.new(key, AES.MODE_CBC, iv)
    file_size = get_file_size(in_file)

    with open(in_file, 'rb') as infile:
        with open(out_file, 'wb') as outfile:
            outfile.write(struct.pack('<Q', file_size))
            outfile.write(iv)

            while True:
                chunk = infile.read(chunk_size)
                if len(chunk) == 0:
                    break
                elif len(chunk) % 16 != 0:
                    chunk += b' ' * (16 - len(chunk) % 16)

                outfile.write(encryptor.encrypt(chunk))


def decrypt_file(key_path, in_file, out_file=None, chunk_size=24 * 1024):
    if not out_file:
        out_file = in_file[:-4]

    key = get_key(key_path)
    with open(in_file, 'rb') as infile:
        orig_size = struct.unpack('<Q', infile.read(struct.calcsize('Q')))[0]
        iv = infile.read(16)
        decryptor = AES.new(key, AES.MODE_CBC, iv)

        with open(out_file, 'wb') as outfile:
            while True:
                chunk = infile.read(chunk_size)
                if len(chunk) == 0:
                    break
                outfile.write(decryptor.decrypt(chunk))

            outfile.truncate(orig_size)
