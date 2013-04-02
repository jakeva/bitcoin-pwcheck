#!/usr/bin/env python

# Bitcoin wallet keys AES encryption / decryption (see http://github.com/joric/pywallet)
# Uses pycrypto or libssl or libeay32.dll or aes.py from http://code.google.com/p/slowaes

crypter = None

try:
    from Crypto.Cipher import AES
    crypter = 'pycrypto'
except:
    pass

class Crypter_pycrypto( object ):
    def SetKeyFromPassphrase(self, vKeyData, vSalt, nDerivIterations, nDerivationMethod):
        data = vKeyData + vSalt
        for i in range(nDerivIterations):
            data = hashlib.sha512(data).digest()
        self.SetKey(data[0:32])
        self.SetIV(data[32:32+16])
        return len(data)

    def SetKey(self, key):
        self.chKey = key

    def SetIV(self, iv):
        self.chIV = iv[0:16]

    def Encrypt(self, data):
        return AES.new(self.chKey,AES.MODE_CBC,self.chIV).encrypt(data)[0:32]

    def Decrypt(self, data):
        return AES.new(self.chKey,AES.MODE_CBC,self.chIV).decrypt(data)[0:32]

try:
    if not crypter:
        import ctypes
        import ctypes.util
        ssl = ctypes.cdll.LoadLibrary (ctypes.util.find_library ('ssl') or 'libeay32')
        crypter = 'ssl'
except:
    pass

class Crypter_ssl(object):
    def __init__(self):
        self.chKey = ctypes.create_string_buffer (32)
        self.chIV = ctypes.create_string_buffer (16)

    def SetKeyFromPassphrase(self, vKeyData, vSalt, nDerivIterations, nDerivationMethod):
        strKeyData = ctypes.create_string_buffer (vKeyData)
        chSalt = ctypes.create_string_buffer (vSalt)
        return ssl.EVP_BytesToKey(ssl.EVP_aes_256_cbc(), ssl.EVP_sha512(), chSalt, strKeyData,
            len(vKeyData), nDerivIterations, ctypes.byref(self.chKey), ctypes.byref(self.chIV))

    def SetKey(self, key):
        self.chKey = ctypes.create_string_buffer(key)

    def SetIV(self, iv):
        self.chIV = ctypes.create_string_buffer(iv)

    def Encrypt(self, data):
        buf = ctypes.create_string_buffer(len(data) + 16)
        written = ctypes.c_int(0)
        final = ctypes.c_int(0)
        ctx = ssl.EVP_CIPHER_CTX_new()
        ssl.EVP_CIPHER_CTX_init(ctx)
        ssl.EVP_EncryptInit_ex(ctx, ssl.EVP_aes_256_cbc(), None, self.chKey, self.chIV)
        ssl.EVP_EncryptUpdate(ctx, buf, ctypes.byref(written), data, len(data))
        output = buf.raw[:written.value]
        ssl.EVP_EncryptFinal_ex(ctx, buf, ctypes.byref(final))
        output += buf.raw[:final.value]
        return output

    def Decrypt(self, data):
        buf = ctypes.create_string_buffer(len(data) + 16)
        written = ctypes.c_int(0)
        final = ctypes.c_int(0)
        ctx = ssl.EVP_CIPHER_CTX_new()
        ssl.EVP_CIPHER_CTX_init(ctx)
        ssl.EVP_DecryptInit_ex(ctx, ssl.EVP_aes_256_cbc(), None, self.chKey, self.chIV)
        ssl.EVP_DecryptUpdate(ctx, buf, ctypes.byref(written), data, len(data))
        output = buf.raw[:written.value]
        ssl.EVP_DecryptFinal_ex(ctx, buf, ctypes.byref(final))
        output += buf.raw[:final.value]
        return output

try:
    if not crypter:
        from aes import *
        crypter = 'pure'
except:
    pass

class Crypter_pure(object):
    def __init__(self):
        self.m = AESModeOfOperation()
        self.cbc = self.m.modeOfOperation["CBC"]
        self.sz = self.m.aes.keySize["SIZE_256"]

    def SetKeyFromPassphrase(self, vKeyData, vSalt, nDerivIterations, nDerivationMethod):
        data = vKeyData + vSalt
        for i in range(nDerivIterations):
            data = hashlib.sha512(data).digest()
        self.SetKey(data[0:32])
        self.SetIV(data[32:32+16])
        return len(data)

    def SetKey(self, key):
        self.chKey = [ord(i) for i in key]

    def SetIV(self, iv):
        self.chIV = [ord(i) for i in iv]

    def Encrypt(self, data):
        mode, size, cypher = self.m.encrypt(data, self.cbc, self.chKey, self.sz, self.chIV)
        return ''.join(map(chr, cypher))

    def Decrypt(self, data):
        chData = [ord(i) for i in data]
        return self.m.decrypt(chData, self.sz, self.cbc, self.chKey, self.sz, self.chIV)

import hashlib

def Hash(data):
    return hashlib.sha256(hashlib.sha256(data).digest()).digest()

def main():

    #address
    # addr = '1ty14WKJtKnC3izG6dh34jqSfinZkSm61'
    # sec = '5JMhGPWc3pkdgPd9jqVZkRtEp3QB3Ze8ihv62TmmvzABmkNzBHw'
    # secret = '47510706d76bc74a5d57bdcffc68c9bbbc2d496bef87c91de7f616129ac62b5f'.decode('hex')
    pubkey = '03ff4c23dcbab571448b5d5d447d1f743308818e5e9a83ca95457fe894a3149851'.decode('hex')
    ckey = 'b5543b930f9b83e2767163dd49ff3dfb936e34b023290d18c550b5e12a7bf510232177b382994f9df23791d3fcef42da'.decode('hex')

    #master key
    crypted_key = '982a07407ccb8d70514e7b7ccae4b53d68318ec41fd2bf99bf9dbcafd2f150a92c6eb8f9ea743b782fc5b85403421c1d'.decode('hex')
    salt = 'b29a2e128e8e0a2f'.decode('hex')
    rounds = 29731
    method = 0
    password = 'animal28'

    global crypter

    if crypter == 'pycrypto':
        crypter = Crypter_pycrypto()
    elif crypter == 'ssl':
        crypter = Crypter_ssl()
        print "using ssl"
    elif crypter == 'pure':
        crypter = Crypter_pure()
        print "using slowaes"
    else:
        print("Need pycrypto of libssl or libeay32.dll or http://code.google.com/p/slowaes")
        exit(1)

    crypter.SetKeyFromPassphrase(password, salt, rounds, method)
    masterkey = crypter.Decrypt(crypted_key)
    crypter.SetKey(masterkey)
    crypter.SetIV(Hash(pubkey))
    d = crypter.Decrypt(ckey)
    e = crypter.Encrypt(d)

    print "masterkey:", masterkey.encode('hex')
    print 'c:', ckey.encode('hex')
    print 'd:', d.encode('hex')
    print 'e:', e.encode('hex')

if __name__ == '__main__':
    main()
