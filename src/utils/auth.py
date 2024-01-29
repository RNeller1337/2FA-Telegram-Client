import base64
import hashlib
import hmac
import struct
import time


def get_hotp_token(secret, intervals_no):
    key = base64.b32decode(normalize(secret), True)
    msg = struct.pack(">Q", intervals_no)
    h = bytearray(hmac.new(key, msg, hashlib.sha1).digest())
    o = h[19] & 15
    h = str((struct.unpack(">I", h[o:o + 4])[0] & 0x7fffffff) % 1000000)
    return prefix0(h)


def get_totp_token(secret):
    return get_hotp_token(secret, intervals_no=int(time.time()) // 30)


def normalize(key):
    k2 = key.strip().replace(' ', '')
    if len(k2) % 8 != 0:
        k2 += '=' * (8 - len(k2) % 8)
    return k2


def prefix0(h):
    if len(h) < 6:
        h = '0' * (6 - len(h)) + h
    return h


def start(secret: str):
    return get_totp_token(secret)
