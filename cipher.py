import time
import sys
import click

from src.cipher_file import *


@click.group()
def main():
    try:
        pass
    except CypherException as e:
        print(str(e))
    except Exception as e:
        print(str(e))


@main.command('e')
@click.option('-in', '--in_file', type=click.Path(exists=True), required=True, help='Input file path')
@click.option('-out', '--out_file', type=click.Path(), help='Output file path')
@click.option('-k', '--key', type=click.Path(), help='Key file path, where rnd key will be stored')
def enc_file(in_file, out_file, key):
    """Encrypt file"""
    t0 = time.time()
    encrypt_file(get_abs_path(key), get_abs_path(in_file), get_abs_path(out_file))
    t1 = time.time()
    elapsed_time = t1 - t0
    click.echo(click.style(f"Done in: {elapsed_time:0.3f} seconds", fg='blue', bold=True))


@main.command('d')
@click.option('-k', '--key', type=click.Path(exists=True), required=True, help='Key file path')
@click.option('-in', '--in_file', type=click.Path(exists=True), required=True, help='Input file path')
@click.option('-out', '--out_file', type=click.Path(), help='Output file path')
def enc_file(key, in_file, out_file):
    """Decrypt file"""
    t0 = time.time()
    decrypt_file(get_abs_path(key), get_abs_path(in_file), get_abs_path(out_file))
    t1 = time.time()
    elapsed_time = t1 - t0
    click.echo(click.style(f"Done in: {elapsed_time:0.3f} seconds", fg='blue', bold=True))


if __name__ == '__main__':
    args = sys.argv
    if "--help" in args or len(args) == 1:
        click.echo("Cipher CLI")
    main()