from PyQt6.QtCore import Qt, QRect
from PyQt6.QtWidgets import QLabel, QWidget, QApplication, QLineEdit
from PyQt6.QtGui import QPixmap, QFont
import sys

class Window(QWidget):
    def __init__(self):
        super().__init__()

        self.setGeometry(1100, 200, 450, 550)
        self.setWindowTitle("LogIn")

        # Label1
        label1 = QLabel(self)
        label1.setGeometry(30, 30, 370, 480)
        label1.setStyleSheet("border-image: url(D:/PyQt/SnowTree.jpg);\n"
                             "border-radius: 20px;")
        label1.setScaledContents(True)

        # Label2
        label2 = QLabel(self)
        label2.setGeometry(30, 30, 370, 480)
        label2.setStyleSheet("background-color: qlineargradient(spread: pad, x1:0, y1:0, y2:0.715909, stop:0 rgba(0, 0, 0, 9), stop:0.375 rgba(0, 0, 0, 50), stop:0.835227 rgba(0, 0, 0, 75)\n"
                             "border-radius: 20px;")

        # Label3
        label3 = QLabel(self)
        label3.setGeometry(50, 60, 330, 450)
        label3.setStyleSheet("background-color: rgba(0, 0, 0, 75);\n"
                             "border-radius: 15px;")

        # Label4
        label4 = QLabel(self)
        label4.setGeometry(QRect(170, 90, 90, 45))
        font = QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(200)
        label4.setFont(font)
        label4.setStyleSheet("color: rgba(255, 255, 255, 210);")
        label4.setText("Log In")

        # LineEdit1
        lineEdit_User = QLineEdit(self)
        lineEdit_User.setGeometry(QRect(115, 180, 200, 30))
        font = QFont()
        font.setPointSize(10)
        lineEdit_User.setFont(font)
        lineEdit_User.setStyleSheet("background-color: rgba(0, 0, 0, 0);\n"
                               "border: none;\n"
                               "border-bottom: 2px solid rgba(155, 168, 182, 255);\n"
                               "color: rgba(255, 255, 255, 255);\n"
                               "padding-bottom: 7px;")
        lineEdit_User.setPlaceholderText(" User Name")

        # LineEdit2
        lineEdit_Pass = QLineEdit(self)
        lineEdit_Pass.setGeometry(QRect(115, 260, 200, 30))
        font = QFont()
        font.setPointSize(10)
        lineEdit_Pass.setFont(font)
        lineEdit_Pass.setStyleSheet("background-color: rgba(0, 0, 0, 0);\n"
                               "border: none;\n"
                               "border-bottom: 2px solid rgba(155, 168, 182, 255);\n"
                               "color: rgba(255, 255, 255, 255);\n"
                               "padding-bottom: 7px;")
        lineEdit_Pass.setPlaceholderText(" Password")

app = QApplication(sys.argv)
window = Window()
window.show()
sys.exit(app.exec())
