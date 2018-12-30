from Crypto.Cipher import AES

key = b'(key)'
cipher = AES.new(key, AES.MODE_ECB)


def encrypt(msg):
    pad = msg + ((16 - len(msg) % 16) * '{')
    return cipher.encrypt(pad.encode("utf-8"))


def decrypt(msg):
    dec = cipher.decrypt(msg).decode('utf-8')
    l = dec.count('{')
    return dec[:len(dec) - l]
