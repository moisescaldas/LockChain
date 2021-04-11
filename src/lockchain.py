from sys import prefix
from typing import Union
from rsa import key, newkeys, PublicKey, PrivateKey
from os import PathLike
from hashlib import sha256
import secrets

class CryptMessage:
    def __init__(self, data : bytes = b"", key : Union[PrivateKey, PublicKey] = None) -> None:
        self.data = data
        self.key = key
    
    def set_data(self, data : bytes = b"") -> bool:
        if type(data) != bytes:
            return False
        
        else:
            self.data = data
            return True

    def set_key(self, key : Union[PrivateKey, PublicKey]) -> bool:
        if type(key) == PrivateKey:
            self.key = key
        
            return True
            
        elif type(key) == PublicKey:
            self.key = key
        
            return True
            
        else:
            
            return False
        
    def get(self) -> bytes:
        return self.data

    def encrypt(self) -> bool:
        if type(self.key) != PrivateKey and type(self.key):
            return False
        
        length_key = length_int(self.key.n)
        length_segment = length_key - 72
        data_segments = []
        data = b''
        
        for i in range(0, (length_data := len(self.data)), length_segment):
            if  not (i + length_segment < length_data):
                data_segments.append(self.data[i:])
            
            else:
                data_segments.append(self.data[i:i + length_segment])
                
        for segment in data_segments:
            verificador = sha256(segment).digest()
            
            frame = verificador + segment
            value = bytes_int(frame)
            calc = pow(value, self.key.e, self.key.n)
            
            data += int.to_bytes(calc, length_key, 'big')
        
        self.data = data
        return True

    def decrypt(self):
        if type(self.key) != PrivateKey:
            return False
        
        length_key = length_int(self.key.n)
        length_segment = length_key - 72
        data_segments = []
        data = b''
        
        for i in range(0, (length_data := len(self.data)), length_key):
            if not (i + length_key < length_data):
                data_segments.append(self.data[i:])
            
            else:  
                data_segments.append(self.data[i:i + length_key])

        for segment in data_segments:
            value = bytes_int(segment)
            calc = pow(value, self.key.d, self.key.n)
            packet = int_bytes(calc)
            
            verificador = packet[:32]
            frame = packet[-length_segment:]

            data += frame
        
        self.data = data
        return True
            
class CryptFile(CryptMessage):
    def __init__(self, file: PathLike = "", key: Union[PrivateKey, PublicKey] = None) -> None:        
        try:
            with open(file, 'rb') as by_file:
                data = by_file.read()
            
        except:
            data = b""
                
        super().__init__(data, key)

        self.file = file

    def set_file(self, file: PathLike) -> bool:
        try:
            with open(file, 'rb') as by_file:
                data = by_file.read()
            
        except FileNotFoundError:
            return False
        
        self.data = data
        return True

    def encrypt(self) -> bool:
        try:
            if super().encrypt():
                with open(self.file, "wb") as by_file:
                    by_file.write(self.data)

                return True
            
            else:
                return False
            
        except:
            return False

    def decrypt(self) -> bool:
        try:
            if super().decrypt():
                with open(self.file, "wb") as by_file:
                    by_file.write(self.data)
                    
                    return True
            
            else:
                return False
        
        except:
            return False


def length_int(num : int = 0) -> int:
    bits = int.bit_length(num)
    
    if not bits % 8:
        return bits // 8
    
    else:
        return (bits // 8) + 1

int_bytes = lambda x : int.to_bytes(x, length_int(x), 'big')
bytes_int = lambda x: int.from_bytes(x, 'big')