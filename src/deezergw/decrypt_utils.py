from hashlib import md5
from binascii import a2b_hex
from Crypto.Cipher import AES
from Crypto.Hash import HMAC, SHA256
from Crypto.Cipher.Blowfish import new as new_blowfish, MODE_CBC

SECRET_KEY = "g4el58wc0zvf9na1"
SOMETHING = a2b_hex("0001020304050607")

HMAC_KEY = SECRET_KEY.encode()
AES_KEY = (SOMETHING * 3)[3:19]


def iter_bytes(data: bytes, chunk_size: int = 2048):
    for start in range(0, len(data), chunk_size):
        yield data[start : start + chunk_size]


def md5hex(data: str):
    return md5(data.encode()).hexdigest()


def calc_bf_key(track_id: str):
    h = md5hex(track_id)

    return "".join(
        chr(ord(h[i]) ^ ord(h[i + 16]) ^ ord(SECRET_KEY[i])) for i in range(16)
    )


def blowfish_decrypt(data: bytes, key: str):
    c = new_blowfish(key.encode(), MODE_CBC, SOMETHING)

    return c.decrypt(data)


# State Encryption


def encrypt(data: str, key: str):
    hmac = HMAC.new(HMAC_KEY + key.encode(), digestmod=SHA256)
    cipher = AES.new(AES_KEY, AES.MODE_CTR)

    ciphertext = cipher.encrypt(data.encode())
    tag = hmac.update(cipher.nonce + ciphertext).digest()

    return tag + cipher.nonce + ciphertext


def decrypt(data: bytes, key: str):
    tag = data[0:32]
    nonce = data[32:40]
    ciphertext = data[40:]

    hmac = HMAC.new(HMAC_KEY + key.encode(), digestmod=SHA256)
    hmac.update(nonce + ciphertext).verify(tag)

    cipher = AES.new(AES_KEY, AES.MODE_CTR, nonce=nonce)
    message = cipher.decrypt(ciphertext)

    return message.decode()
