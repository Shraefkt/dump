from Crypto.Cipher import AES
from Crypto.Hash import HMAC, SHA256
from Crypto.Random import get_random_bytes
import pickle

DOC_LEN = 100
K = get_random_bytes(32)
test_ds = [b"b"*DOC_LEN for x in range(5)]

def Enc(K,DS):
    SE_K, CHF_K = K[:16], K[16:]
    EDS = dict()

    for i in range(len(DS)):
        IV = get_random_bytes(8)
        cipher = AES.new(SE_K, AES.MODE_CTR, nonce=IV)
        C = IV + cipher.encrypt(DS[i])
        hash = HMAC.new(CHF_K, digestmod=SHA256)
        hash.update(bytes((i)))
        tk = hash.digest()
        EDS[tk] = C

    return pickle.dumps(EDS)

def Token(K,i :int):
    SE_K, CHF_K = K[:16], K[16:]
    hash = HMAC.new(CHF_K, digestmod=SHA256)
    hash.update(bytes((i)))
    return hash.digest()

def Dec(K,C):
    if C is None:
        return None
    SE_K, CHF_K = K[:16], K[16:]
    IV, SE_C = C[:8], C[8:]
    cipher = AES.new(SE_K, AES.MODE_CTR, nonce=IV)
    D = cipher.decrypt(SE_C)
    return D

def Search(tk,EDS :bytes):
    EDS = pickle.loads(EDS)
    if tk in EDS.keys():
        return EDS[tk]
    else:
        return None
assert Dec(K,Search(Token(K,3),Enc(K,test_ds))) == test_ds[3]
