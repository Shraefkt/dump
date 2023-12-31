from Crypto.Cipher import AES
from Crypto.Hash import HMAC, SHA256
from Crypto.Random import get_random_bytes
import pickle
import math
import time

n = int(input("insert number of documents: "))
dl = int(input("insert length of document: "))
d = math.ceil(math.log(n,2))+1 # number of layers
K = get_random_bytes(32)

def Enc(K,DS :list):
    SE_K, CHF_K = K[:16], K[16:]
    EDS = dict()
    for i in range(pow(2,(d-1)),pow(2,d)): #all leaf nodes
        hash = HMAC.new(CHF_K, digestmod=SHA256)
        hash.update(bytes(i))
        tk = hash.digest()
        if i < 2**(d-1) + n: # real node
            real_i = i - 2**d
            IV = get_random_bytes(8)
            cipher = AES.new(SE_K, AES.MODE_CTR, nonce=IV)
            C = IV + cipher.encrypt(DS[real_i])
        else: # padded node
            C = '0' * 16
        EDS[tk] = C
    return pickle.dumps(EDS)

def Token(K,i :int):
    SE_K, CHF_K = K[:16], K[16:]
    depth_node = math.floor(math.log(i,2))+1
    x_node = d - depth_node  # depth to leaf layer
    tk_list = []
    for tk_i in range((i)*2**x_node,(i+1)*2**x_node): #documents to encrypt
        hash = HMAC.new(CHF_K, digestmod=SHA256)
        hash.update(bytes((tk_i)))
        tk = hash.digest()
        tk_list.append(tk)
    return pickle.dumps(tk_list)

def Dec(K,C_list :list):
    SE_K, CHF_K = K[:16], K[16:]
    D_list = []
    for C in C_list:
        IV , SE_C = C[:8],C[8:]
        if IV == '00000000':
            D_list.append(None)
        else:
            cipher = AES.new(SE_K, AES.MODE_CTR, nonce=IV)
            D_list.append(cipher.decrypt(SE_C))
    return D_list


def Search(tk_list: bytes,EDS :bytes):
    tk_list = pickle.loads(tk_list)
    EDS = pickle.loads(EDS)
    D_list = []
    for tk in tk_list:
        if tk in EDS.keys():
            D_list.append(EDS[tk])
        else:
            pass
    return D_list


test_ds = [bytes(str(i)*dl,'utf-8') for i in range(2**(d-1),2**(d))]

st = time.process_time()
test = lambda i :Dec(K,Search(Token(K,i),Enc(K,test_ds)))
for i in range(2**(d-1),2**(d)):
    print(i, test(i))
et = time.process_time()
print(f"Storage length: {len(Enc(K,test_ds))}")
print(f"Average bandwidth/total data sent: {len(Enc(K,test_ds))/n+len(Token(K,i))}") #what does it actually refer to

print(f"Total time: {time.process_time()} seconds")
print(f"Average query time: {(et-st)/2**d} seconds")


print(f"Total time: {time.process_time()} seconds")
print(f"Average query time: {(et-st)/2**d} seconds")
