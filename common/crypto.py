import math
import random
import sympy
def generate_keys():
    """RSA avec sympy pour grands nombres premiers"""
    p = sympy.randprime(1000, 10000)
    q = sympy.randprime(1000, 10000)
    while q == p:
        q = sympy.randprime(1000, 10000)
    
    n = p * q
    phi = (p - 1) * (q - 1)
    
    e = 65537
    while math.gcd(e, phi) != 1:
        e += 2
    
    d = pow(e, -1, phi)
    return ((e, n), (d, n))
def encrypt(message: str, public_key):
    """Chiffre un message par blocs de 3 caracteres"""
    e, n = public_key
    
    blocks = []
    for i in range(0, len(message), 3):
        block = message[i:i+3]
        num = 0
        for j, c in enumerate(block):
            num += ord(c) * (256 ** j)
        
        encrypted_num = pow(num, e, n)
        blocks.append(str(encrypted_num))
    
    return ','.join(blocks)
def decrypt(data, private_key):
    """Dechiffre un message chiffre par blocs"""
    d, n = private_key
    
    try:
        blocks = [int(x) for x in data.split(',')]
        result = []
        
        for encrypted_num in blocks:
            decrypted_num = pow(encrypted_num, d, n)
            
            # Extraire les 3 caracteres du bloc
            chars = []
            for _ in range(3):
                if decrypted_num > 0:
                    char_code = decrypted_num % 256
                    if char_code > 0:
                        chars.append(chr(char_code))
                    decrypted_num //= 256
            
            result.extend(chars)
        
        return ''.join(result)
        
    except Exception as e:
        print(f"Erreur decrypt: {e}")
        return None