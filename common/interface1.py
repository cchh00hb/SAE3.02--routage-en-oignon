import sys
from PySide6.QtWidgets import QApplication, QLabel, QMainWindow

class TestWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Test Affichage Debian -> Windows")
        label = QLabel("Si tu vois ce message, c'est que ça marche !")
        label.setMargin(20)
        self.setCentralWidget(label)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TestWindow()
    window.show()
    sys.exit(app.exec())