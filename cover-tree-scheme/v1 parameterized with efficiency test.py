from Crypto.Cipher import AES
from Crypto.Hash import HMAC, SHA256
from Crypto.Random import get_random_bytes
import pickle
import math
import time

n = int(input("insert number of documents"))
dl = int(input("insert length of document"))
d = math.ceil(math.log(n,2))+1
K = get_random_bytes(32)
def Enc(K,DS):
    SE_K, CHF_K = K[:16], K[16:]
    EDS = dict()
    for i in range(1,pow(2,d)): #all nodes
        depth_node = math.floor(math.log(i,2))+1
        x_node = d - depth_node # depth to leaf layer
        C_list = []
        for d_i in range(i*pow(2,x_node),(i+1)*pow(2,x_node)): #documents to encrypt
            if d_i < 2 ** (d - 1) + n:
                real_i = d_i - 2**d
                IV = get_random_bytes(8)
                cipher = AES.new(SE_K, AES.MODE_CTR, nonce=IV)
                C = IV + cipher.encrypt(DS[real_i])
                C_list.append(C)
            else:
                C_list.append('0000000000000000')
        hash = HMAC.new(CHF_K, digestmod=SHA256)
        hash.update(bytes(i))
        tk = hash.digest()
        EDS[tk] = C_list
    return pickle.dumps(EDS)

def Token(K,i :int):
    SE_K, CHF_K = K[:16], K[16:]
    hash = HMAC.new(CHF_K, digestmod=SHA256)
    hash.update(bytes((i)))
    return hash.digest()

def Dec(K,C_list):
    if C_list is None:
        return None
    SE_K, CHF_K = K[:16], K[16:]
    D_list = []
    for C in C_list:
        IV, SE_C = C[:8], C[8:]
        if IV == '00000000':
            D_list.append(None)
        else:
            cipher = AES.new(SE_K, AES.MODE_CTR, nonce=IV)
            D_list.append(cipher.decrypt(SE_C))
    return D_list

def Search(tk,EDS :bytes):
    EDS = pickle.loads(EDS)
    if tk in EDS.keys():
        return EDS[tk]
    else:
        return None

test_ds = [bytes(str(i)*dl,'utf-8') for i in range(2**(d-1),2**d)]


st = time.process_time()
test = lambda i :Dec(K,Search(Token(K,i),Enc(K,test_ds)))
for i in range(1,2**d):
    print(i, test(i))
et = time.process_time()
print(f"Storage length: {len(Enc(K,test_ds))}")
print(f"Average bandwith/total data sent: {(len(Enc(K,test_ds))/n+len(Token(K,i)))}")


print(f"Total time: {time.process_time()} seconds")
print(f"Average query time: {(et-st)/n} seconds")
