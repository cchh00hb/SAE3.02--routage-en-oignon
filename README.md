# SAE 3.02 - Architecture Distribuée avec Routage en Oignon
Ce projet implémente un système de communication anonyme de type "Tor" (Onion Routing) entre un Client A et un Client B via un circuit de 3 routeurs virtuels.

## Vidéo de démonstration
Le fonctionnement complet du système est visible ici : 👉 https://youtu.be/MLcqnxFoloY

## Architecture du Système
Le projet est déployé de manière distribuée sur deux machines virtuelles Debian :

Machine 1 (Debian 1 - 192.168.1.80) :

Master : Serveur d'annuaire qui gère l'enregistrement des routeurs et la distribution des clés publiques.

Routeur 1 (R1) & Routeur 2 (R2) : Nœuds de routage.

Client A : Interface graphique (PySide6) permettant de construire l'oignon et d'envoyer le message.

Machine 2 (Debian 2 - 192.168.1.65) :

Routeur 3 (R3) : Nœud de sortie

Client B : Destinataire final (Bob) qui reçoit le message en clair.

## Chiffrement et Anonymisation
Algorithme : RSA simplifié implémenté  (sans bibliothèques de crypto externes).

Principe : Le Client A récupère les clés publiques du Master, puis chiffre le message en 3 couches successives. Chaque routeur ne possède que sa clé privée et 
ne peut déchiffrer qu'une seule couche, ne connaissant ainsi que le saut précédent et le saut suivant.

# Installation et Déploiement
1. Prérequis sur les deux VM


sudo apt update && sudo apt install python3 python3-pip git -y
pip install PySide6

2. Récupération du code

git clone https://github.com/cchh00hb/SAE3.02--routage-en-oignon.git
//se mettre a la racine du projet 
cd /opt/sae3.02-routageoignon/SAE3.02--routage-en-oignon

3. Configuration de l'environnement (IMPORTANT)
Python nécessite que la racine du projet soit dans le chemin de recherche des modules. Exécutez cette commande dans chaque nouveau terminal :


export PYTHONPATH=$PYTHONPATH:.


Guide de Lancement (Ordre à respecter)

Sur Debian 1 (Terminal 1) : Démarrer le Master

Bash

python3 -m master.master
Sur Debian 2 (Terminal 1) : Démarrer le Destinataire (Client B)

Bash

python3 -m client.clientB
Sur Debian 2 (Terminal 2) : Démarrer le Routeur 3

Bash

python3 -m router.router R3 9003 192.168.1.80
Sur Debian 1 (Terminaux 2 & 3) : Démarrer les Routeurs 1 et 2

Bash

python3 -m router.router R1 9001 192.168.1.80
python3 -m router.router R2 9002 192.168.1.80
Sur Debian 1 (Terminal 4) : Lancer l'Interface Graphique (Client A)

Bash

python3 -m common.interface_v3

# Notes Techniques
Base de données : Pour des raisons de portabilité et de stabilité réseau lors des tests, la gestion des routeurs et des clés est effectuée en mémoire (dictionnaire Python) par le Master au lieu d'une base MariaDB.

Dépannage : Si un port est bloqué, utilisez fuser -k [PORT]/tcp pour libérer le processus.

Auteur
Chahinez F - BUT Réseaux & Télécoms
