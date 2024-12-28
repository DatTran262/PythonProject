from PyQt6.QtCore import Qt, QRect
from PyQt6.QtWidgets import QLabel, QWidget, QApplication, QLineEdit, QGraphicsDropShadowEffect, QPushButton
from PyQt6.QtGui import QPixmap, QFont, QColor, QIcon
import sys

class Window(QWidget):
    def __init__(self):
        super().__init__()

        self.setGeometry(1500, 200, 450, 550) #laptop 1100, PC 1500
        self.setWindowTitle("LogIn")
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        # Label1
        label1 = QLabel(self)
        label1.setGeometry(30, 30, 370, 480)
        label1.setStyleSheet("border-image: url(D:/Code/PyCharm/Images/background.jpg);\n"
                             "border-radius: 20px;")
        label1.setScaledContents(True)
        label1.setGraphicsEffect(QGraphicsDropShadowEffect(blurRadius=25, xOffset=0, yOffset=0, color=QColor(234, 221, 186, 100)))

        # Label2
        label2 = QLabel(self)
        label2.setGeometry(30, 30, 370, 480)
        label2.setStyleSheet("background-color: qlineargradient(spread: pad, x1:0, y1:0, y2:0.715909, stop:0 rgba(0, 0, 0, 9), stop:0.375 rgba(0, 0, 0, 50), stop:0.835227 rgba(0, 0, 0, 75)\n"
                             "border-radius: 20px;")

        # Label3
        label3 = QLabel(self)
        label3.setGeometry(40, 60, 350, 450)
        label3.setStyleSheet("background-color: rgba(0, 0, 0, 75);\n"
                             "border-radius: 15px;")
        label3.setGraphicsEffect(QGraphicsDropShadowEffect(blurRadius=25, xOffset=0, yOffset=0, color=QColor(105, 221, 132, 100)))

        # Label4
        label4 = QLabel(self)
        label4.setGeometry(QRect(170, 90, 90, 45))
        font = QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(1000)
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
        lineEdit_Pass.setEchoMode(QLineEdit.EchoMode.Password)
        lineEdit_Pass.setPlaceholderText(" Password")

        # Button Login
        buttonLogIn = QPushButton(self)
        buttonLogIn.setGeometry(QRect(115, 340, 200, 45))
        buttonLogIn.setObjectName("buttonLogin")  # Gán objectName phù hợp
        buttonLogIn.setStyleSheet("""
            QPushButton#buttonLogin {
                background-color: qlineargradient(spread:pad, x1:0, y1:0.505682, x2:1, y2:0.477, 
                                                  stop:0 rgba(20, 47, 78, 219), stop:1 rgba(85, 98, 112, 226));
                color: rgba(255, 255, 255, 210);
                border-radius: 5px;
            }
            QPushButton#buttonLogin:hover {
                background-color: qlineargradient(spread:pad, x1:0, y1:0.505682, x2:1, y2:0.477, 
                                                  stop:0 rgba(40, 67, 98, 219), stop:1 rgba(105, 118, 132, 226));
            }
            QPushButton#buttonLogin:pressed {
                background-color: rgba(105, 118, 132, 200);
                padding-left: 5px;
                padding-top: 5px;
            }
        """)
        buttonLogIn.setText("L o g I n")
        font = QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(700)
        buttonLogIn.setFont(font)

        # Label forgot
        label5 = QLabel(self)
        label5.setGeometry(QRect(115, 375, 200, 45))
        label5.setText("Forgot your User Name or Password?")
        label5.setStyleSheet("color: rgba(255, 255, 255, 140);")
        label5.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Button Facebook
        btnFace = QPushButton(self)
        btnFace.setGeometry(QRect(115, 435, 40, 40))
        btnFace.setIcon(QIcon("D:/Code/PyCharm/Images/icon-facebook.svg"))


app = QApplication(sys.argv)
window = Window()
window.show()
sys.exit(app.exec())
