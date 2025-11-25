import math
import random


"""source et aide : github simple rsa encryption"""
def is_prime(n):
    """verifie si un nombre est premier"""
    if n <= 1:
        return False
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True



def generate_keys():
    """génère une paire de clés publique et privée"""
    p = 0
    q = 0
    while not is_prime(p):
        p = random.randint(11, 50)
    while not is_prime(q) or q == p:
        q = random.randint(11, 50)

    n = p * q
    phi = (p - 1) * (q - 1)

    e = 3
    while math.gcd(e, phi) != 1:
        e += 2

    d = pow(e, -1, phi)
    return ((e, n), (d, n))


"""chiffre le message avec la clé publique"""
def encrypt(message: str, public_key):
    
    e, n = public_key
    data = [pow(ord(c), e, n) for c in message]
    return data 


"""déchiffre un message avec la clé privée"""
def decrypt(data, private_key):


    d, n = private_key
    message = ''.join([chr(pow(c, d, n)) for c in data])
    return message
