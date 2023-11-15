from Crypto.Cipher import AES
from Crypto.Hash import HMAC, SHA256
from Crypto.Random import get_random_bytes
import pickle
import math
import time

class DocumentLookupSchemeClient:
    def __init__(self,DS:list):
        self.DS = DS #document set
        self.n = len(DS) #num of documents
        self.dl = len(DS[0]) # document length (fixed)
        self.d = math.ceil(math.log(self.n,2))+1 # number of layers
        self.K = get_random_bytes(32) #Key (SE_K + CHF_K)
        self.SE_K, self.CHF_K = self.K[:16], self.K[16:]
        self.cache = dict()

    def CHF(self,key,input):
        hash = HMAC.new(key, digestmod=SHA256)
        hash.update(bytes((input)))
        return hash.digest()

    def get_hash(self,i): #i is node number in binary tree
        if i in self.cache.keys() :
            return self.cache[i]
        if i == 1:
            h = self.CHF_K
        elif i % 2 == 0:
            h = self.CHF(self.get_hash(math.floor(i / 2)), 0)
        else:
            h = self.CHF(self.get_hash(math.floor(i / 2)), 1)
        self.cache[i] = h
        return h

    def Enc(self):
        EDS = dict()
        for i in range(self.n):  # no of documents
            IV = get_random_bytes(8)
            cipher = AES.new(self.SE_K, AES.MODE_CTR, nonce=IV)
            EDS[self.get_hash(2**(d-1) + i)] = IV + cipher.encrypt(self.DS[i] + bytes(str(i),'utf-8')) #maybe add padding later
        del self.DS
        return pickle.dumps(EDS)

    def Token(self,i):
        return self.get_hash(i)

    def over_cover(self,a,b,debug=False):
        if a > self.n or b > self.n or a > b or a < 0 :
            return None
        a = a + 2 ** (self.d - 1) - 1
        b = b + 2 ** (self.d - 1) - 1
        shift_length = len("{:b}".format(a^b)) if a!=b else 0
        node = a >> shift_length
        if debug:
            print(f"Node: {node}")
            print(f"a: {a}, b: {b}, n: {self.n}")
        return self.Token(node)

    def Dec(self,CS,a,b,debug=False):
        DS = []
        CS = pickle.loads(CS)
        if CS == None:
            return None
        for C in CS:
            if C is None:
                return None #returned in order, so decryption can just stop
            IV, SE_C = C[:8], C[8:]
            cipher = AES.new(self.SE_K, AES.MODE_CTR, nonce=IV)
            D_m = cipher.decrypt(SE_C)
            # error handling?? but problem should be to do with length of D_m
            D_n,n = D_m[:self.dl], D_m[self.dl:]
            if a <= int(n)+1 <= b:
                DS.append(D_n)
        if debug:
            print(f"{CS}")
            print(f"{DS}")
        return DS

class DocumentLookupSchemeServer:
    def __init__(self,EDS,depth):
        self.EDS = pickle.loads(EDS) # encrypted document set
        self.depth = depth

    def CHF(self,key,input):
        hash = HMAC.new(key, digestmod=SHA256)
        hash.update(bytes((input)))
        return hash.digest()

    def Search(self,tk):
        if tk is None:
            return pickle.dumps(None)
        return pickle.dumps(self.recurse(self.depth, [tk]))

    def recurse(self,depth,lis):
        if lis[0] in self.EDS.keys(): # leaf nodes reached
                return [self.EDS[l] for l in lis if l in self.EDS.keys()]
        if depth == 0:
            return None
        else:
            return self.recurse(depth - 1, [f(l) for l in lis for f in (lambda x: self.CHF(x, 0), lambda x: self.CHF(x, 1))])

n = int(input("insert number of documents: "))
dl = int(input("insert length of document: "))
d = math.ceil(math.log(n,2))+1 # number of layers

test_ds = [bytes((str(i-2**(d-1)+1)*dl)[:dl],'utf-8') for i in range(2**(d-1),2**(d-1)+n)]

client = DocumentLookupSchemeClient(test_ds)
server = DocumentLookupSchemeServer(client.Enc(),d)

while True:
    a = int(input("a:"))
    b = int(input("b:"))
    print(client.Dec(server.Search(client.over_cover(a,b)),a,b))
