""" Do encrypt and decrypt for internal API data transfer for Simplex.

It uses 3DES encryption, and hexlify returning values(input values too).
"""
import re
import string
import random
import mcrypt
import binascii

RE_KEY = re.compile(r"ssl\.key=(.+)")
m = mcrypt.MCRYPT('tripledes', 'cfb')
keyfile = "/root/conf/server.conf"

def plain_key(keyfile):
    """ Return plain ssl key in keyfile

    >>> plain_key('/root/conf/server.conf')
    '$_simplex_$'

    >>> plain_key('/root/conf/serve')
    Traceback (most recent call last):
        ...
    IOError: [Errno 2] No such file or directory: '/root/conf/serve'
    """

    for line in open(keyfile).readlines():
        key = RE_KEY.match(line)
        if key:
            return key.group(1)

def key(keyfile):
    """ Return padded ssl key in keyfile

    >>> key('/root/conf/server.conf')
    '$_simplex_$\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00'

    >>> key('/root/conf/serve')
    Traceback (most recent call last):
        ...
    IOError: [Errno 2] No such file or directory: '/root/conf/serve'
    """
    key = plain_key(keyfile)
    for x in range(0, (24 - len(key))):
        key = key + "\0"
    return key


def generate_iv(length):
    """ Generates iv for 3des encryption

    >>> iv = generate_iv(8)
    >>> len(iv)
    8
    """
    return ''.join([random.choice(string.ascii_letters + string.digits) \
                    for x in range(length)])

def decrypt(text, iv):
    """ Return decrypted text 

    >>> decrypt(text='d19e4374', iv='c35532e8cbc764d6')
    'test'
    """
    iv = binascii.unhexlify(iv)
    m.init(key(keyfile), iv)
    return m.decrypt(binascii.unhexlify(text))

def encrypt(text):
    """ Return encrypted text

    >>> result = encrypt('The quick brown fox jumps over the lazy dog')
    >>> decrypt(text=result['text'], iv=result['hexlified_iv'])
    'The quick brown fox jumps over the lazy dog'
    """
    iv_size = m.get_iv_size()
    iv = generate_iv(iv_size)
    m.init(key(keyfile), iv)
    text = m.encrypt(text)
    return {"hexlified_iv": binascii.hexlify(iv),
            "text": binascii.hexlify(text)}

if __name__ == "__main__":
    import doctest
    doctest.testmod()
