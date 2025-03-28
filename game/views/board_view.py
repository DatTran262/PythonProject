from PyQt6.QtWidgets import QWidget, QPushButton, QGridLayout, QLabel, QVBoxLayout
from PyQt6.QtCore import Qt, QPropertyAnimation, QPoint
from PyQt6.QtGui import QColor, QPalette
from PyQt6.QtWidgets import QGraphicsDropShadowEffect

class BoardView(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.layout = QVBoxLayout()
        self.setStyleSheet("background-color: #FFFFFF;")
        
        # Status label
        self.status_label = QLabel("Player X's Turn")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setStyleSheet("""
            QLabel {
                font-size: 20px;
                color: #B8860B;
                padding: 10px;
                border-radius: 10px;
                background: #FFFAF0;
            }
        """)
        
        # Add golden shadow effect to status label
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(15)
        shadow.setColor(QColor('#FFD700'))
        shadow.setOffset(0, 0)
        self.status_label.setGraphicsEffect(shadow)
        
        # Grid for buttons
        self.grid = QGridLayout()
        self.buttons = [[None for _ in range(3)] for _ in range(3)]
        
        for i in range(3):
            for j in range(3):
                self.buttons[i][j] = QPushButton()
                self.buttons[i][j].setFixedSize(100, 100)
                self.buttons[i][j].setStyleSheet("""
                    QPushButton {
                        font-size: 40px;
                        font-weight: bold;
                        background: #FFFAF0;
                        border-radius: 10px;
                        border: 2px solid #B8860B;
                    }
                    QPushButton:hover {
                        background: #FFE4B5;
                    }
                """)
                
                # Add golden shadow to buttons
                button_shadow = QGraphicsDropShadowEffect()
                button_shadow.setBlurRadius(10)
                button_shadow.setColor(QColor('#FFD700'))
                button_shadow.setOffset(0, 0)
                self.buttons[i][j].setGraphicsEffect(button_shadow)
                
                self.grid.addWidget(self.buttons[i][j], i, j)

        self.layout.addWidget(self.status_label)
        self.layout.addLayout(self.grid)
        self.setLayout(self.layout)

    def update_button(self, row, col, symbol):
        self.buttons[row][col].setText(symbol)

    def update_status(self, text):
        self.status_label.setText(text)

    def reset_board(self):
        for i in range(3):
            for j in range(3):
                self.buttons[i][j].setText('')