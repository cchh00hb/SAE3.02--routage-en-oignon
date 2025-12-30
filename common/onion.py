import random
from common.crypto import encrypt, decrypt

def dechiffrer_couche(message_chiffre, cle_privee):
    """Dechiffre une couche d'oignon"""
    couche_claire = decrypt(message_chiffre, cle_privee)
    
    if not couche_claire:
        return None
    
    # Cas 1: NEXT:RX|DATA:...
    if couche_claire.startswith("NEXT:") and "|DATA:" in couche_claire:
        next_part, data_part = couche_claire.split("|DATA:", 1)
        routeur = next_part[5:]
        return "NEXT", routeur, data_part
    
    # Cas 2: DEST:IP:PORT|MSG:...
    elif couche_claire.startswith("DEST:") and "|MSG:" in couche_claire:
        dest_part, msg_part = couche_claire.split("|MSG:", 1)
        destinataire = dest_part[5:]
        return "DEST", destinataire, msg_part
    
    # Cas 3: Format non reconnu
    return "UNKNOWN", "", couche_claire

def choisir_chemin_aleatoire(routeurs_disponibles, nb_sauts=3):
    """Choisit un chemin aleatoire de routeurs"""
    if not routeurs_disponibles:
        return []
    
    if len(routeurs_disponibles) < nb_sauts:
        nb_sauts = len(routeurs_disponibles)
    
    return random.sample(routeurs_disponibles, nb_sauts)

def construire_oignon(message, destinataire, chemin_routeurs, cles_publiques):
    """Construit un oignon"""
    couche = f"DEST:{destinataire}|MSG:{message}"
    
    for i in range(len(chemin_routeurs)-1, -1, -1):
        routeur = chemin_routeurs[i]
        
        if i == len(chemin_routeurs)-1:
            couche = encrypt(couche, cles_publiques[routeur])
        else:
            prochain = chemin_routeurs[i+1]
            couche_claire = f"NEXT:{prochain}|DATA:{couche}"
            couche = encrypt(couche_claire, cles_publiques[routeur])
        
        if not couche:
            return None
    
    return couche
