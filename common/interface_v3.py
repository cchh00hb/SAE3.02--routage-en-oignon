import sys
import os
import threading
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                               QHBoxLayout, QTextEdit, QLineEdit, QPushButton, QLabel)
from PySide6.QtCore import Qt


from common.network import send_message
from common.onion import construire_oignon

class ClientGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.keys = {}
        
        self.master_ip = "192.168.1.80"  # Debian 1
        self.dest_default = "192.168.1.65:8888"  # Debian 2
        
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("SAE 3.02 - Client A (Interface Oignon)")
        self.setGeometry(100, 100, 700, 500)
        
        central_widget = QWidget()
        layout = QVBoxLayout()

        # --- Section Master ---
        master_layout = QHBoxLayout()
        self.lbl_master = QLabel(f"P du master: {self.master_ip}")
        self.btn_keys = QPushButton("1. récuperer les clés")
        self.btn_keys.clicked.connect(self.get_keys)
        master_layout.addWidget(self.lbl_master)
        master_layout.addWidget(self.btn_keys)
        layout.addLayout(master_layout)

        # --- Zone de Logs ---
        layout.addWidget(QLabel("Console"))
        self.log_area = QTextEdit()
        self.log_area.setReadOnly(True)
        
        layout.addWidget(self.log_area)

        # --- Section Envoi ---
        layout.addWidget(QLabel("Destinataire Final (IP:PORT) :"))
        self.dest_in = QLineEdit(self.dest_default)
        layout.addWidget(self.dest_in)

        layout.addWidget(QLabel("Message :"))
        self.msg_in = QLineEdit()
        self.msg_in.setPlaceholderText("Tapez votre message...")
        layout.addWidget(self.msg_in)
        self.btn_send = QPushButton("2. envoyer le message")
        self.btn_send.clicked.connect(self.send_msg)
        layout.addWidget(self.btn_send)

        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def log(self, message):
        self.log_area.append(f"> {message}")

    def get_keys(self):
        self.log("récupération des clés des routeur...")
       
        res = send_message(self.master_ip, 8000, "GET_KEYS")
        
        if res and res != "NO_ROUTERS":
            try:
               
                self.keys = {}
                for item in res.split(';'):
                    if ':' in item:
                        rid, key_data = item.split(':')
                        e, n = map(int, key_data.split(','))
                        self.keys[rid] = (e, n)
                
                self.log(f"Routeurs trouvés : {list(self.keys.keys())}")
            except Exception as e:
                self.log(f"Erreur formatage clés : {e}")
        else:
            self.log("ERREUR : Aucun routeur n'est enregistré sur le master?")

    def send_msg(self):
        message = self.msg_in.text()
        destination = self.dest_in.text()
        
        if not self.keys:
            self.log("ERREUR : il faut d'abord récupérer les clés !")
            return
        
        if not message:
            self.log("ERREUR : Le message est vide.")
            return

        chemin = ["R1", "R2", "R3"]
        
        self.log(f"destination :  {destination}...")
        try:
           
            oignon = construire_oignon(message, destination, chemin, self.keys)
            
            if oignon:
                self.log("Oignon généré")
                
                reponse = send_message("192.168.1.80", 9001, oignon)
                
                if reponse:
                    self.log(f"Réponse du circuit : votre message a bien été reçu par le destinataire final")
                else:
                    self.log("Pas de réponse de R1 (Vérifiez qu'il est lancé).")
        except Exception as e:
            self.log(f"Erreur lors de la construction : {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ClientGUI()
    window.show()
    sys.exit(app.exec())