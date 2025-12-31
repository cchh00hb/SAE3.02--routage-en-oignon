# SAE 3.02 - Conception d'une architecture distribuée avec routage en oignon

Ce projet implémente un système de communication anonyme entre un Client A et un Client B à travers un circuit de 3 routeurs virtuels (R1, R2, R3) répartis sur deux machines Debian.

## Vidéo de démonstration
**Regardez le fonctionnement complet  : https://youtu.be/MLcqnxFoloY

## Architecture du Réseau
Le projet est déployé sur deux machines virtuelles :
* **Debian 1 (192.168.1.80)** : Master, Routeur 1, Routeur 2, Client A (Interface Qt).
* **Debian 2 (192.168.1.65)** : Routeur 3, Client B (Récepteur).

## Installation

### 1. Prérequis
```bash
sudo apt update && sudo apt install python3 python3-pip -y
pip install PySide6

