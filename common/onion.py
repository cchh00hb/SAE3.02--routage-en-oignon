import random
from common.crypto import encrypt, decrypt

def construire_oignon(message, destinataire, chemin_routeurs, cles_publiques):

    print(f"Construction oignon avec chemin: {chemin_routeurs}")
    
   
    couche_actuelle = f"DEST:{destinataire}|MSG:{message}"
    print(f"Couche interne: {couche_actuelle}")
    
    for i in range(len(chemin_routeurs)-1, -1, -1):
        routeur = chemin_routeurs[i]
        
        if i == len(chemin_routeurs)-1:
           
            couche_actuelle = encrypt(couche_actuelle, cles_publiques[routeur])
        else:
            
            next_hop = chemin_routeurs[i+1]
            couche_claire = f"NEXT:{next_hop}|DATA:{couche_actuelle}"
            couche_actuelle = encrypt(couche_claire, cles_publiques[routeur])
    
    return couche_actuelle

def dechiffrer_couche(message_chiffre, cle_privee):

    couche_claire = decrypt(message_chiffre, cle_privee)
    print(f"Couche dechiffree: {couche_claire}")
    
    if couche_claire.startswith("NEXT:"):
        parts = couche_claire.split("|")
        next_hop = parts[0].replace("NEXT:", "")
        data = parts[1].replace("DATA:", "")
        return "NEXT", next_hop, data
        
    elif couche_claire.startswith("DEST:"):
        parts = couche_claire.split("|")
        destinataire = parts[0].replace("DEST:", "")
        message = parts[1].replace("MSG:", "")
        return "DEST", destinataire, message
        
    return "UNKNOWN", "", couche_claire

def choisir_chemin_aleatoire(routeurs_disponibles, nb_sauts=3):
    """Choisit un chemin aleatoire de routeurs"""
    if len(routeurs_disponibles) < nb_sauts:
        nb_sauts = len(routeurs_disponibles)
    
    return random.sample(routeurs_disponibles, nb_sauts)