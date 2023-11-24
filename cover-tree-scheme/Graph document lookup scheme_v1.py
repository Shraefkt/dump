from Crypto.Cipher import AES
from Crypto.Hash import HMAC, SHA256
from Crypto.Random import get_random_bytes
import pickle
import math

K = get_random_bytes(32)
def Enc(K,DS):
    SE_K, CHF_K = K[:16], K[16:]
    EDS = dict()
    len_DS = len(DS)
    depth = math.ceil(math.log(len_DS,2)) + 1 # defined as layers of nodes
    for i in range(1,pow(2,depth)): #all nodes
        depth_node = math.floor(math.log(i,2))
        x_node = depth - depth_node - 1 # depth to leaf layer
        C_list = []
        for d_i in range(i*pow(2,x_node),(i+1)*pow(2,x_node)): #documents to encrypt
            real_d_i_pos_in_DS = d_i - (len_DS)
            IV = get_random_bytes(8)
            cipher = AES.new(SE_K, AES.MODE_CTR, nonce=IV)
            C = IV + cipher.encrypt(DS[real_d_i_pos_in_DS])
            C_list.append(C)
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
        cipher = AES.new(SE_K, AES.MODE_CTR, nonce=IV)
        D_list.append(cipher.decrypt(SE_C))
    return D_list

def Search(tk,EDS :bytes):
    EDS = pickle.loads(EDS)
    if tk in EDS.keys():
        return EDS[tk]
    else:
        return None

test_ds = [bytes(str(i)*100,'utf-8') for i in range(8,16)]
test = lambda i :Dec(K,Search(Token(K,i),Enc(K,test_ds)))
for i in range(1,16):
    print(i, test(i))
print(f"Storage length: {len(Enc(K,test_ds))}")
