import sys
from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtCore import Qt
from models.board_model import BoardModel
from views.board_view import BoardView
from controllers.game_controller import GameController

class TicTacToeWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Tic Tac Toe Game")
        self.setStyleSheet("background-color: #FFFFFF;")
        
        # Create MVC components
        self.model = BoardModel()
        self.view = BoardView()
        self.controller = GameController(self.model, self.view)
        
        # Set up main window
        self.setCentralWidget(self.view)
        self.setFixedSize(400, 500)
        self.center_window()

    def center_window(self):
        # Center window on screen
        screen = QApplication.primaryScreen().geometry()
        size = self.geometry()
        self.move(
            (screen.width() - size.width()) // 2,
            (screen.height() - size.height()) // 2
        )

if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    # Set application-wide attributes
    app.setStyle('Fusion')
    
    window = TicTacToeWindow()
    window.show()
    
    sys.exit(app.exec())