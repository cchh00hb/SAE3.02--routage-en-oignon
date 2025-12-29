import sys
import os
import threading
from datetime import datetime

# Ajout du dossier parent au chemin pour trouver le module 'common'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Changement des imports PyQt5 vers PySide6
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                               QHBoxLayout, QTextEdit, QLineEdit, QPushButton, 
                               QLabel, QSpinBox, QGroupBox, QMessageBox)
from PySide6.QtCore import Signal, QObject # Signal remplace pyqtSignal
from PySide6.QtGui import QFont

from common.network import start_server, send_message
from common.crypto import encrypt

class MessageReceiver(QObject):
    message_received = Signal(str) # Changé en Signal
    
    def __init__(self, port):
        super().__init__()
        self.port = port
        self.running = False
    
    def start(self):
        self.running = True
        thread = threading.Thread(target=self._run_server, daemon=True)
        thread.start()
    
    def _run_server(self):
        def handle_message(msg):
            timestamp = datetime.now().strftime("%H:%M:%S")
            self.message_received.emit(f"[{timestamp}] {msg}")
            return "MESSAGE_RECU"
        
        start_server(self.port, handle_message)

class ClientGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.master_ip = "192.168.56.102"
        self.master_port = 8000
        self.my_port = 8888
        self.keys = {}
        
        self.init_ui()
        self.start_receiver()
    
    def init_ui(self):
        self.setWindowTitle("Client Onion Router")
        self.setGeometry(100, 100, 700, 600)
        
        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QVBoxLayout(central)
        
        # Configuration
        config_group = QGroupBox("Configuration")
        config_layout = QVBoxLayout()
        
        port_layout = QHBoxLayout()
        port_layout.addWidget(QLabel("Port d'ecoute:"))
        self.port_input = QSpinBox()
        self.port_input.setRange(1024, 65535)
        self.port_input.setValue(self.my_port)
        port_layout.addWidget(self.port_input)
        port_layout.addStretch()
        config_layout.addLayout(port_layout)
        
        master_layout = QHBoxLayout()
        master_layout.addWidget(QLabel("Master:"))
        self.master_input = QLineEdit(f"{self.master_ip}:{self.master_port}")
        master_layout.addWidget(self.master_input)
        self.connect_button = QPushButton("Recuperer les cles")
        self.connect_button.clicked.connect(self.get_keys)
        master_layout.addWidget(self.connect_button)
        config_layout.addLayout(master_layout)
        
        self.status_label = QLabel("Statut: Non connecte")
        config_layout.addWidget(self.status_label)
        
        config_group.setLayout(config_layout)
        main_layout.addWidget(config_group)
        
        # Messages recus
        received_group = QGroupBox("Messages recus")
        received_layout = QVBoxLayout()
        self.received_text = QTextEdit()
        self.received_text.setReadOnly(True)
        self.received_text.setMaximumHeight(200)
        received_layout.addWidget(self.received_text)
        received_group.setLayout(received_layout)
        main_layout.addWidget(received_group)
        
        # Envoi de message
        send_group = QGroupBox("Envoyer un message")
        send_layout = QVBoxLayout()
        
        dest_layout = QHBoxLayout()
        dest_layout.addWidget(QLabel("Destinataire:"))
        self.dest_input = QLineEdit()
        self.dest_input.setPlaceholderText("IP:Port (ex: 192.168.56.102:8888)")
        dest_layout.addWidget(self.dest_input)
        send_layout.addLayout(dest_layout)
        
        send_layout.addWidget(QLabel("Message:"))
        self.message_input = QTextEdit()
        self.message_input.setMaximumHeight(100)
        send_layout.addWidget(self.message_input)
        
        self.send_button = QPushButton("Envoyer via R1 -> R2 -> R3")
        self.send_button.clicked.connect(self.send_message)
        self.send_button.setEnabled(False)
        send_layout.addWidget(self.send_button)
        
        send_group.setLayout(send_layout)
        main_layout.addWidget(send_group)
        
        # Logs
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setMaximumHeight(150)
        main_layout.addWidget(QLabel("Logs:"))
        main_layout.addWidget(self.log_text)
    
    def start_receiver(self):
        self.receiver = MessageReceiver(self.my_port)
        self.receiver.message_received.connect(self.display_received_message)
        self.receiver.start()
        self.log(f"Serveur demarre sur port {self.my_port}")
    
    def get_keys(self):
        self.log("Recuperation des cles depuis le master...")
        
        try:
            parts = self.master_input.text().split(':')
            master_ip = parts[0]
            master_port = int(parts[1])
            
            resp = send_message(master_ip, master_port, "GET_KEYS")
            
            if not resp:
                self.log("ERREUR: Pas de reponse du master")
                return
            
            self.keys = {}
            for item in resp.split(';'):
                if ':' in item:
                    rid, k = item.split(':')
                    e, n = map(int, k.split(','))
                    self.keys[rid] = (e, n)
            
            self.log(f"Cles recuperees: {list(self.keys.keys())}")
            self.status_label.setText(f"Statut: Connecte - {len(self.keys)} routeurs")
            self.send_button.setEnabled(True)
            
        except Exception as e:
            self.log(f"ERREUR: {e}")
            self.status_label.setText("Statut: Erreur de connexion")
    
    def send_message(self):
        dest = self.dest_input.text().strip()
        msg = self.message_input.toPlainText().strip()
        
        if not dest or not msg:
            QMessageBox.warning(self, "Erreur", "Destinataire et message requis")
            return
        
        if len(self.keys) < 3:
            QMessageBox.warning(self, "Erreur", "Pas assez de routeurs (besoin de 3)")
            return
        
        self.log(f"Construction de l'oignon pour: {dest}")
        self.log(f"Message: {msg}")
        
        try:
            # Construction de l'oignon (Couches de chiffrement RSA successives)
            couche3 = f"DEST:{dest}|MSG:{msg}"
            ch3 = encrypt(couche3, self.keys['R3'])
            
            couche2 = f"NEXT:R3|DATA:{ch3}"
            ch2 = encrypt(couche2, self.keys['R2'])
            
            couche1 = f"NEXT:R2|DATA:{ch2}"
            oignon = encrypt(couche1, self.keys['R1'])
            
            self.log(f"Oignon construit: {len(oignon)} caracteres")
            
            # Envoi a R1 (Premier saut du routage)
            result = send_message("192.168.56.102", 9001, oignon)
            
            if result:
                self.log(f"Reponse: {result}")
                QMessageBox.information(self, "Succes", "Message envoye !")
                self.message_input.clear()
            else:
                self.log("ERREUR: Pas de reponse de R1")
                QMessageBox.warning(self, "Erreur", "Echec d'envoi")
                
        except Exception as e:
            self.log(f"ERREUR: {e}")
            QMessageBox.critical(self, "Erreur", f"Erreur lors de l'envoi: {e}")
    
    def display_received_message(self, msg):
        self.received_text.append(msg)
    
    def log(self, msg):
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_text.append(f"[{timestamp}] {msg}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ClientGUI()
    window.show()
    sys.exit(app.exec()) # Retrait de l'underscore pour PySide6