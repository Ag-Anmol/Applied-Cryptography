'''
Trivium Stream Cipher Key Stream Assignment
'''


from bitstring import BitArray

# Class to generate the keystream
class TriviumCipher:
    # All members are private
    __key = [0]*80
    __IV = [0]*80
    __first = [0]*93
    __second = [0]*84
    __third = [0]*111
    __t1 = 0
    __t2 = 0
    __t3 = 0
    __z = 0

    def __init__(self,k : str,IV : str):

        # checking the size of key and IV

        if(len(k)<80):
            s = "0"*(80-len(k))
            k = s+k
        else:
            k = k[:80]

        if(len(IV)<80):
            s = "0"*(80-len(IV))
            IV = s+IV
        else:
            IV = IV[:80]

        # Initialising first, second and third with key and IV

        self.__key = list(map(int,list(k)))
        self.__IV = list(map(int,list(IV)))
        self.__first = self.__key + [0 for i in range(13)]
        self.__second = self.__IV + [0 for i in range(177 - 80 - 93)]
        self.__third[-3::] = [1,1,1]

        # 4 full rounds before starting
        [self.genKey() for i in range(4*288)]

    # Function to storing the logic of new bits generation as per Trivium Cipher Algorithm 
    def __operations(self):
        self.__t1 = self.__first[66-1] ^ self.__first[93-1]
        self.__t2 = self.__second[162 - 93 - 1] ^ self.__second[177 - 93 - 1]
        self.__t3 = self.__third[243 - 84 - 93 - 1] ^ self.__third[288 - 84 - 93 - 1]
        
        self.__z = self.__t1 ^ self.__t2 ^ self.__t3

        self.__t1 = self.__t1  ^ (self.__first[91 - 1] & self.__first[92 - 1]) ^ self.__second[171 - 93 - 1]
        self.__t2 = self.__t2  ^ (self.__second[175 - 93 - 1] & self.__second[176 - 93 - 1]) ^ self.__third[264 - 84 - 93 - 1]
        self.__t3 = self.__t3  ^ (self.__third[286 - 84 - 93 - 1] & self.__third[287 - 84 - 93 - 1]) ^ self.__first[69 - 1]

        self.__first = [self.__t3] + self.__first[:-1]
        self.__second = [self.__t1] + self.__second[:-1]
        self.__third = [self.__t2] + self.__third[:-1]

    # Public Function to generate the encryption bit 
    def genKey(self) -> int:
        self.__operations()
        return self.__z
    
    # Function to generate n sized keystream for encryption
    def keystream(self, n):
        stream = ""
        for i in range(n):
            stream = str(self.genKey()) + stream
        
        stream = "0b" + stream
        hex_keystream = BitArray(stream)
        hex_keystream.byteswap()                # for byte swapping in pair of 2
        return "0x" + hex_keystream.hex.upper()


k = input("enter the Key (with 0x___) : ").replace(" ","")
iv = input("enter the IV (with 0x___) : ").replace(" ","")
n = int(input("size of key stream (int value) : "))

KEY = BitArray(hex=k)
KEY.byteswap()
KEY = str(bin(int(str(KEY)[2:],16)))[2:]

IV = BitArray(hex=iv)
IV.byteswap()
IV = str(bin(int(str(IV)[2:],16)))[2:]

c = TriviumCipher(KEY,IV)
print("KEYSTREAM :", c.keystream(n))
