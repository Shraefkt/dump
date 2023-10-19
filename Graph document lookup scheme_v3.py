from Crypto.Cipher import AES
from Crypto.Hash import HMAC, SHA256
from Crypto.Random import get_random_bytes
import pickle
import math

K = get_random_bytes(32)
def Enc(K,DS :list):
    SE_K, CHF_K = K[:16], K[16:]
    EDS = dict()
    len_DS = len(DS)
    depth = math.ceil(math.log(len_DS,2)) + 1 # defined as layers of nodes
    for i in range(pow(2,(depth-1)),pow(2,depth)): #all leaf nodes
            real_i = i - len_DS
            IV = get_random_bytes(8)
            cipher = AES.new(SE_K, AES.MODE_CTR, nonce=IV)
            C = IV + cipher.encrypt(DS[real_i])
            hash = HMAC.new(CHF_K, digestmod=SHA256)
            hash.update(bytes(i))
            tk = hash.digest()
            EDS[tk] = C
    return pickle.dumps(EDS)

def Token(K,i :int,EDS): #technically doesn't meet the definition
    SE_K, CHF_K = K[:16], K[16:]
    depth = math.ceil(math.log(len(EDS), 2)) + 1
    depth_node = math.floor(math.log(i,2))
    x_node = depth - depth_node - 1 # depth to leaf layer
    tk_list = []
    for tk_i in range(i*pow(2,x_node),(i+1)*pow(2,x_node)): #documents to encrypt
        hash = HMAC.new(CHF_K, digestmod=SHA256)
        hash.update(bytes((tk_i)))
        tk = hash.digest()
        tk_list.append(tk)
    return pickle.dumps(tk_list)

def Dec(K,C_list :list):
    if C_list is None:
        return None
    SE_K, CHF_K = K[:16], K[16:]
    D_list = []
    for C in C_list:
        IV, SE_C = C[:8], C[8:]
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

test_ds = [bytes(str(i)*100,'utf-8') for i in range(8,16)]
test = lambda i :Dec(K,Search(Token(K,i,test_ds),Enc(K,test_ds)))
for i in range(1,16):
    print(i, test(i))
print(f"Storage length: {len(Enc(K,test_ds))}")
