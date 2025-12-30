import sys
import os
import threading
from datetime import datetime

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                               QHBoxLayout, QTextEdit, QLineEdit, QPushButton, 
                               QLabel, QSpinBox, QGroupBox, QMessageBox)
from PySide6.QtCore import Signal, QObject
from PySide6.QtGui import QFont

from common.network import start_server, send_message
from common.crypto import encrypt

class MessageReceiver(QObject):
    message_received = Signal(str)
    def __init__(self, port):
        super().__init__()
        self.port = port
        
    def start(self):
        thread = threading.Thread(target=self._run_server, daemon=True)
        thread.start()
        
    def _run_server(self):
        def handle_message(msg):
            self.message_received.emit(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}")
            return "OK"
        start_server(self.port, handle_message)

class ClientGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.keys = {}
        # PORT CHANGÉ ICI : 9999 au lieu de 8888
        self.listen_port = 9999 
        
        self.init_ui()
        self.start_receiver()
        
    def init_ui(self):
        self.setWindowTitle("Client Onion Router - SAE")
        self.setGeometry(100, 100, 600, 500)
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        
        # En-tête de statut du port
        status_layout = QHBoxLayout()
        self.port_label = QLabel(f"Serveur d'écoute actif sur le port : {self.listen_port}")
        self.port_label.setStyleSheet("color: green; font-weight: bold;")
        status_layout.addWidget(self.port_label)
        layout.addLayout(status_layout)

        # Zone des messages reçus
        self.received_text = QTextEdit()
        self.received_text.setReadOnly(True)
        layout.addWidget(QLabel("Messages reçus :"))
        layout.addWidget(self.received_text)
        
        # Bouton de test
        self.btn = QPushButton("Tester l'affichage")
        self.btn.clicked.connect(lambda: QMessageBox.information(self, "Succès", f"L'interface est opérationnelle sur le port {self.listen_port} !"))
        layout.addWidget(self.btn)

    def start_receiver(self):
        # Initialisation du récepteur sur le port 9999
        self.receiver = MessageReceiver(self.listen_port)
        self.receiver.message_received.connect(lambda m: self.received_text.append(m))
        self.receiver.start()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ClientGUI()
    window.show()
    sys.exit(app.exec())