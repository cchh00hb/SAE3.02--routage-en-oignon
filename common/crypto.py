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
    """génère une paire de clés publique et privée (rsa)"""
    p = 0
    q = 0
    while not is_prime(p): #boucle jusqua obtenir un nombre p
        p = random.randint(11, 50) #choix aleatoire de p, la plage et petite alors a revoir plus tard pour la secutité
    while not is_prime(q) or q == p: # boucle pour q premier et different de p
        q = random.randint(11, 50)

    n = p * q #produit de p et q (des premiers)
    phi = (p - 1) * (q - 1) #fonctiond'euler

    e = 3
    while math.gcd(e, phi) != 1:  # Incrémente e jusqu'à ce qu'il soit copremier avec phi
        e += 2

    d = pow(e, -1, phi)  # Inverse modulaire de e modulo phi (clé privée)
    return ((e, n), (d, n))# Retourne clé publique (e,n) et privée (d,n)


"""chiffre le message avec la clé publique"""
def encrypt(message: str, public_key):
    e, n = public_key # Extrait e et n de la clé publique
    # (formule RSA : c = m^e mod n)
    data = [pow(ord(c), e, n) for c in message]  # Liste d'entiers chiffrés (un par char)
    return ','.join(str(x) for x in data)


"""déchiffre un message avec la clé privée"""
def decrypt(data, private_key):
    d, n = private_key
    
    if isinstance(data, str):
        data_list = [int(x) for x in data.split(',')]
    else:
        data_list = data
    message = ''.join([chr(pow(c, d, n)) for c in data_list])
    return message