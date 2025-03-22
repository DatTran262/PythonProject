# view.py
from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QPainter, QColor, QFont

class FlappyBirdView(QWidget):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.model = controller.model
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Flappy Bird')
        self.setGeometry(300, 300, self.model.screen_width, self.model.screen_height)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_game)
        self.timer.start(20)  # Cập nhật mỗi 20ms (~50 FPS)

    def update_game(self):
        self.controller.update()
        self.update()  # Gọi paintEvent để vẽ lại

    def paintEvent(self, event):
        painter = QPainter(self)
        
        # Vẽ nền
        painter.fillRect(0, 0, self.model.screen_width, self.model.screen_height, QColor(135, 206, 235))

        # Vẽ ống
        painter.setBrush(QColor(0, 255, 0))
        for pipe in self.model.pipes:
            # Ống trên
            painter.drawRect(pipe["x"], 0, self.model.pipe_width, pipe["top"])
            # Ống dưới
            painter.drawRect(pipe["x"], pipe["bottom"], self.model.pipe_width, self.model.screen_height - pipe["bottom"])

        # Vẽ chim
        painter.setBrush(QColor(255, 255, 0))
        painter.drawEllipse(self.model.bird_x, int(self.model.bird_y), self.model.bird_size, self.model.bird_size)

        # Vẽ điểm số
        painter.setFont(QFont("Arial", 20))
        painter.setPen(QColor(255, 255, 255))
        painter.drawText(10, 30, f"Score: {self.model.score}")

        # Vẽ thông báo game over
        if self.model.game_over:
            painter.setFont(QFont("Arial", 30))
            painter.setPen(QColor(255, 0, 0))
            painter.drawText(self.model.screen_width // 4, self.model.screen_height // 2, "Game Over!")

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Space:
            self.controller.jump()
        elif event.key() == Qt.Key.Key_R and self.model.game_over:
            self.controller.reset()