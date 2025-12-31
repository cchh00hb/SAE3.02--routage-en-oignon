# SAE 3.02 - Conception d'une architecture distribuée avec routage en oignon

Ce projet implémente un système de communication anonyme entre un Client A et un Client B à travers un circuit de 3 routeurs virtuels (R1, R2, R3) répartis sur deux machines Debian.

## Vidéo de démonstration
**Regardez le fonctionnement complet  : https://youtu.be/MLcqnxFoloY

## Architecture du Réseau
Le projet est déployé sur deux machines virtuelles :
* **Debian 1 (192.168.1.80)** : Master, Routeur 1, Routeur 2, Client A (Interface Qt).
* **Debian 2 (192.168.1.65)** : Routeur 3, Client B (Récepteur).

## Installation

## 1. Prérequis
```bash
sudo apt update && sudo apt install python3 python3-pip -y
pip install PySide6

## 2. Configuration (À faire dans CHAQUE terminal)
Il est indispensable d'exporter le chemin des modules pour que Python trouve le dossier common :

export PYTHONPATH=$PYTHONPATH:.
Lancement - respecter l'ordre
Sur Debian 1 : Lancer le Master python3 -m master.master

Sur Debian 2 : Lancer le Client B python3 -m client.clientB

Sur Debian 2 : Lancer le Routeur 3 python3 -m router.router R3 9003 192.168.1.80

Sur Debian 1 : Lancer R1 et R2 (dans 2 terminaux) python3 -m router.router R1 9001 192.168.1.80 python3 -m router.router R2 9002 192.168.1.80

Sur Debian 1 : Lancer l'Interface Client A python3 -m common.interface_v3
