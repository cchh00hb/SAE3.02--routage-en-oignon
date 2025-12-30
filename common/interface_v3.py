import sys
import os
import threading
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                               QHBoxLayout, QTextEdit, QLineEdit, QPushButton, QLabel)
from common.network import send_message
from common.onion import construire_oignon

class ClientGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.keys = {}
        self.master_ip = "192.168.1.80" # L'IP de votre Debian 1
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Client A - Interface Oignon")
        self.setGeometry(100, 100, 600, 500)
        
        layout = QVBoxLayout()
        self.log_area = QTextEdit()
        self.log_area.setReadOnly(True)
        
        self.btn_keys = QPushButton("1. Recuperer Cles du Master")
        self.btn_keys.clicked.connect(self.get_keys)
        
        # IP de Debian 2 par défaut
        self.dest_in = QLineEdit("192.168.1.65:8888") 
        self.msg_in = QLineEdit()
        self.msg_in.setPlaceholderText("Tapez votre message ici...")
        self.btn_send = QPushButton("2. Envoyer via Oignon")
        self.btn_send.clicked.connect(self.send_msg)
        
        layout.addWidget(QLabel(f"Master IP: {self.master_ip}"))
        layout.addWidget(self.btn_keys)
        layout.addWidget(self.log_area)
        layout.addWidget(QLabel("Destinataire Final (IP:Port) :"))
        layout.addWidget(self.dest_in)
        layout.addWidget(self.msg_in)
        layout.addWidget(self.btn_send)
        
        central = QWidget()
        central.setLayout(layout)
        self.setCentralWidget(central)

    def get_keys(self):
        res = send_message(self.master_ip, 8000, "GET_KEYS")
        if res and res != "NO_ROUTERS":
            for item in res.split(';'):
                rid, k = item.split(':')
                self.keys[rid] = tuple(map(int, k.split(',')))
            self.log_area.append(f"Cles recuperees pour : {list(self.keys.keys())}")
        else:
            self.log_area.append("Erreur : Aucun routeur ou Master injoignable.")

    def send_msg(self):
        message = self.msg_in.text()
        destination = self.dest_in.text()
        # On définit le chemin des routeurs enregistrés sur le Master
        chemin = ["R1", "R2", "R3"] 
        
        oignon = construire_oignon(message, destination, chemin, self.keys)
        if oignon:
            # Envoi au premier routeur R1 sur Debian 1
            send_message(self.master_ip, 9001, oignon)
            self.log_area.append(f"Message envoye via {chemin}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ClientGUI()
    window.show()
    sys.exit(app.exec())
