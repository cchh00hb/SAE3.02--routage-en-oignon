import random
from common.crypto import encrypt, decrypt  # Import des fonctions de chiffrement/déchiffrement (probablement RSA)

def construire_oignon(message, destinataire, chemin_routeurs, cles_publiques):
    """
    Construit un message en oignon avec plusieurs couches de chiffrement
    """
    print(f"Construction oignon avec chemin: {chemin_routeurs}")  # Debug: affiche le chemin choisi
    
    # Commencer par la couche la plus interne (le message final, visible seulement par le destinataire)
    couche_actuelle = f"DEST:{destinataire}|MSG:{message}"
    print(f"Couche interne: {couche_actuelle}")  # Debug: montre la couche de base
    
    # Ajouter les couches en partant de la fin du chemin vers le début (empilement des chiffrages)
    for i in range(len(chemin_routeurs)-1, -1, -1):  # Boucle inverse pour chiffrer de l'extérieur vers l'intérieur
        routeur = chemin_routeurs[i]  # Routeur actuel dans la boucle
        try:
            if i == len(chemin_routeurs)-1:  # Si c'est le dernier routeur (plus proche du destinataire)
                # Il contient directement le message final chiffré
                couche_actuelle = encrypt(couche_actuelle, cles_publiques[routeur])  # Chiffre avec la clé publique du routeur
            else:
                # Routeur intermédiaire: ajoute le prochain saut et chiffre
                next_hop = chemin_routeurs[i+1]  # Prochain routeur dans le chemin
                couche_claire = f"NEXT:{next_hop}|DATA:{couche_actuelle}"  # Format: indique le prochain saut et les données chiffrées
                couche_actuelle = encrypt(couche_claire, cles_publiques[routeur])  # Chiffre la couche entière
        except KeyError:  # Erreur si la clé publique du routeur n'existe pas
            print(f"Erreur: Clé publique manquante pour {routeur}")
            return None  # Arrête la construction si clé manquante
    
    return couche_actuelle  # Retourne l'oignon complet (message multi-couches)

def dechiffrer_couche(message_chiffre, cle_privee):
    """
    Dechiffre une couche d'oignon et retourne les informations
    """
    try:
        couche_claire = decrypt(message_chiffre, cle_privee)  # Déchiffre avec la clé privée du routeur
        print(f"Couche dechiffree: {couche_claire}")  # Debug: affiche ce qui a été déchiffré
        
        if couche_claire.startswith("NEXT:"):  # Si c'est une couche intermédiaire (indique le prochain saut)
            parts = couche_claire.split("|", 1)  # Sépare en 2 parties max (évite les erreurs si "|" dans les données)
            if len(parts) == 2:  # Vérifie que le format est correct
                next_hop = parts[0].replace("NEXT:", "")  # Extrait le prochain routeur
                data = parts[1].replace("DATA:", "")  # Extrait les données chiffrées restantes
                return "NEXT", next_hop, data  # Retourne le type, le saut, et les données
        
        elif couche_claire.startswith("DEST:"):  # Si c'est la couche finale (message pour le destinataire)
            parts = couche_claire.split("|", 1)  # Même parsing
            if len(parts) == 2:
                destinataire = parts[0].replace("DEST:", "")  # Extrait le destinataire
                message = parts[1].replace("MSG:", "")  # Extrait le message
                return "DEST", destinataire, message  # Retourne le type, dest, et message
        
        return "UNKNOWN", "", couche_claire  # Si format inconnu, retourne tel quel
    except Exception as e:  # Capture les erreurs de déchiffrement ou parsing
        print(f"Erreur de déchiffrement: {e}")
        return "ERROR", "", ""  # Retourne un indicateur d'erreur

def choisir_chemin_aleatoire(routeurs_disponibles, nb_sauts=3):
    """Choisit un chemin aleatoire de routeurs"""
    if not routeurs_disponibles:  # Vérifie si la liste est vide
        return []  # Retourne une liste vide si aucun routeur
    
    if len(routeurs_disponibles) < nb_sauts:  # Ajuste si pas assez de routeurs
        nb_sauts = len(routeurs_disponibles)
    
    return random.sample(routeurs_disponibles, nb_sauts)  # Sélectionne aléatoirement sans répétition
