from Crypto.Cipher import AES
from Crypto.Hash import HMAC, SHA256
from Crypto.Random import get_random_bytes
import pickle
import math
import time

class DocumentLookupScheme:
    def __init__(self,DS:list):
        self.DS = DS #document set
        self.n = len(DS) #num of documents
        self.dl = len(DS[0]) # document length (fixed)
        self.d = math.ceil(math.log(self.n,2))+1 # number of layers
        self.K = get_random_bytes(32) #Key (SE_K + CHF_K)
        self.SE_K, self.CHF_K = self.K[:16], self.K[16:]

    def Enc(self):
        EDS = dict()
        for i in range(2,2**d):  # all nodes
            hash = HMAC.new(self.CHF_K, digestmod=SHA256)
            hash.update(bytes(math.floor(i/2)))
            parent_tk = hash.digest()
            if parent_tk not in EDS.keys():
                EDS[parent_tk] = []
            if i < 2**(d-1): # normal node
                hash = HMAC.new(self.CHF_K, digestmod=SHA256)
                hash.update(bytes(i))
                tk = hash.digest()
                EDS[parent_tk].append(
                    tk)
            elif i < 2**(d-1) + n:# real leaf node
                real_i = i - 2 ** d
                IV = get_random_bytes(8)
                cipher = AES.new(self.SE_K, AES.MODE_CTR, nonce=IV)
                C = IV + cipher.encrypt(self.DS[real_i])
                EDS[parent_tk].append(C)
            else: # padded leaf node
                C = '0' * 16
                EDS[parent_tk].append(C)
        self.EDS = EDS
        del self.DS

    def Token(self,i: int):
        hash = HMAC.new(self.CHF_K, digestmod=SHA256)
        hash.update(bytes((i)))
        tk = hash.digest()
        return(tk)
    def Search(self,tk):
        CS = []
        if tk not in self.EDS.keys():
            return [tk]
        tk_to_search_or_C = self.EDS[tk]
        if type(tk_to_search_or_C) is list:
            CS += self.Search(tk_to_search_or_C[0])
            CS += self.Search(tk_to_search_or_C[1])
        return CS
    def Dec(self,CS):
        DS = []
        for C in CS:
            IV, SE_C = C[:8], C[8:]
            if IV == '00000000':
                DS.append(None)
            else:
                cipher = AES.new(self.SE_K, AES.MODE_CTR, nonce=IV)
                DS.append(cipher.decrypt(SE_C))
        return DS

n = int(input("insert number of documents: "))
dl = int(input("insert length of document: "))
d = math.ceil(math.log(n,2))+1 # number of layers

test_ds = [bytes(str(i-2**(d-1)+1)*dl,'utf-8') for i in range(2**(d-1),2**(d))]

st = time.process_time()

scheme = DocumentLookupScheme(test_ds)
scheme.Enc()
test = lambda i :scheme.Dec(scheme.Search(scheme.Token(i)))
total_bandwidth = 0
for i in range(1,2**(d-1)): # can't query leaf nodes
    token = scheme.Token(i)
    server_response = scheme.Search(token)
    total_bandwidth += len(pickle.dumps(server_response)) + len(token)
    print(i,scheme.Dec(server_response))

et = time.process_time()
print(f"Storage length: {len(pickle.dumps(scheme.EDS))}")
print(f"Total data sent: {total_bandwidth}")
print(f"Average data sent: {total_bandwidth/2**(d-1)}")

print(f"Total time: {time.process_time()} seconds")
print(f"Average query time: {(et-st)/2**(d-1)} seconds")