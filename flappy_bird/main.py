# main.py
import sys
from PyQt6.QtWidgets import QApplication
from view import FlappyBirdView
from controller import FlappyBirdController

if __name__ == '__main__':
    app = QApplication(sys.argv)
    controller = FlappyBirdController()
    view = FlappyBirdView(controller) 
    view.show()
    sys.exit(app.exec())