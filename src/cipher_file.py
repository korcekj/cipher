import os
import struct

from Crypto.Cipher import AES
from Crypto import Random


class CypherException(Exception):
    def __init__(self, message):
        # Call the base class constructor with the parameters it needs
        super().__init__(message)


def gen_key(key_size=256):
    return Random.get_random_bytes(key_size // 8)  # 128 bits key


def gen_iv(iv_size=128):
    return Random.get_random_bytes(iv_size // 8)  # 128 bits iv


def is_file(path):
    return os.path.isfile(path)


def get_dir(file):
    if not file:
        return None
    return os.path.dirname(file)


def get_abs_path(file):
    if not file:
        return None
    return os.path.abspath(file)


def get_basename(file):
    if not file:
        return None
    return os.path.basename(file)


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


def encrypt_file(key_path, in_filename, out_filename=None, chunk_size=64 * 1024):
    if not out_filename:
        out_filename = in_filename + '.enc'
    if not key_path:
        key = gen_key()
        out_dir = get_dir(out_filename)
        write_file(join_to_path(out_dir, 'secret.key'), key)
    else:
        key = read_file(key_path)

    iv = gen_iv()
    encryptor = AES.new(key, AES.MODE_CBC, iv)
    file_size = os.path.getsize(in_filename)

    with open(in_filename, 'rb') as infile:
        with open(out_filename, 'wb') as outfile:
            outfile.write(struct.pack('<Q', file_size))
            outfile.write(iv)

            while True:
                chunk = infile.read(chunk_size)
                if len(chunk) == 0:
                    break
                elif len(chunk) % 16 != 0:
                    chunk += b' ' * (16 - len(chunk) % 16)

                outfile.write(encryptor.encrypt(chunk))


def decrypt_file(key_path, in_filename, out_filename=None, chunk_size=24 * 1024):
    if not out_filename:
        out_filename = in_filename[:-4]

    key = read_file(key_path)
    with open(in_filename, 'rb') as infile:
        orig_size = struct.unpack('<Q', infile.read(struct.calcsize('Q')))[0]
        iv = infile.read(16)
        decryptor = AES.new(key, AES.MODE_CBC, iv)

        with open(out_filename, 'wb') as outfile:
            while True:
                chunk = infile.read(chunk_size)
                if len(chunk) == 0:
                    break
                outfile.write(decryptor.decrypt(chunk))

            outfile.truncate(orig_size)
