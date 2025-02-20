from PyQt6.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QGraphicsDropShadowEffect, QApplication
from PyQt6.QtGui import QFont, QColor, QIcon, QDesktopServices
from PyQt6.QtCore import QRect, Qt, QDir, QUrl

class RegisterView(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(1100, 200, 450, 550)
        self.setWindowTitle("Register")
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.initUI()
        self.center()

    def initUI(self):
        self.createBackgroundLabels()
        self.createRegisterComponents()
        self.createSocialButtons()
        self.createExitButton()

    def createBackgroundLabels(self):
        label1 = QLabel(self)
        label1.setGeometry(30, 30, 370, 480)
        label1.setStyleSheet(f"border-image: url({QDir.current().filePath('QLabel/Images/background.jpg')});"
                             "border-radius: 20px;")
        label1.setScaledContents(True)
        label1.setGraphicsEffect(
            QGraphicsDropShadowEffect(blurRadius=25, xOffset=0, yOffset=0, color=QColor(234, 221, 186, 100)))

        label2 = QLabel(self)
        label2.setGeometry(30, 30, 370, 480)
        label2.setStyleSheet("background-color: qlineargradient(spread: pad, x1:0, y1:0, y2:0.715909, "
                             "stop:0 rgba(0, 0, 0, 9), stop:0.375 rgba(0, 0, 0, 50), "
                             "stop:0.835227 rgba(0, 0, 0, 75));"
                             "border-radius: 20px;")

        label3 = QLabel(self)
        label3.setGeometry(40, 60, 350, 450)
        label3.setStyleSheet("background-color: rgba(0, 0, 0, 75);"
                             "border-radius: 15px;")
        label3.setGraphicsEffect(
            QGraphicsDropShadowEffect(blurRadius=25, xOffset=0, yOffset=0, color=QColor(105, 221, 132, 100)))

        label4 = QLabel(self)
        label4.setGeometry(QRect(165, 90, 100, 45))
        label4.setFont(QFont("Times New Roman", 20, QFont.Weight.Bold))
        label4.setStyleSheet("color: rgba(255, 255, 255, 210);")
        label4.setText("Register")

    def createRegisterComponents(self):
        self.txtUser = self.createLineEdit(115, 160, " Email Address or Phone", 10)
        self.txtPassword = self.createLineEdit(115, 225, " Password", 10, echoMode=QLineEdit.EchoMode.Password)
        self.txtConfirmPassword = self.createLineEdit(115, 290, " Confirm Password", 10, echoMode=QLineEdit.EchoMode.Password)

        self.labelNotice = QLabel(self)
        self.labelNotice.setGeometry(QRect(115, 310, 200, 45))
        self.labelNotice.setStyleSheet("color: red;")

        self.buttonRegister = QPushButton(self)
        self.buttonRegister.setGeometry(QRect(115, 350, 200, 45))
        self.buttonRegister.setObjectName("buttonRegister")
        self.buttonRegister.setStyleSheet(self.getRegisterButtonStyle())
        self.buttonRegister.setText("R e g i s t e r")
        self.buttonRegister.setFont(QFont("Times New Roman", 15, QFont.Weight.Bold))

        self.btnSignIn = QPushButton("S i g n I n?", self)
        self.btnSignIn.setGeometry(QRect(180, 405, 70, 20))
        self.btnSignIn.setStyleSheet("""
            QPushButton {
                color: rgba(255, 255, 255, 140);
                background-color: transparent;
                border: none;
            }
            QPushButton:hover {
                color: rgba(0, 200, 255, 255);
            }
            QPushButton:pressed {
                color: rgba(0, 255, 100, 255);
            }
        """)

    def createLineEdit(self, x, y, placeholder, fontSize, echoMode=None):
        lineEdit = QLineEdit(self)
        lineEdit.setGeometry(QRect(x, y, 200, 30))
        lineEdit.setFont(QFont("Times New Roman", fontSize))
        lineEdit.setStyleSheet("background-color: rgba(0, 0, 0, 0);"
                               "border: none;"
                               "border-bottom: 2px solid rgba(155, 168, 182, 255);"
                               "color: rgba(255, 255, 255, 255);"
                               "padding-bottom: 7px;")
        lineEdit.setPlaceholderText(placeholder)
        if echoMode:
            lineEdit.setEchoMode(echoMode)
        return lineEdit

    def getRegisterButtonStyle(self):
        return """
            QPushButton#buttonRegister {
                background-color: qlineargradient(spread: pad, x1:0, y1:0.505682, x2:1, y2:0.477,
                                                  stop:0 rgba(20, 47, 78, 219), stop:1 rgba(85, 98, 112, 226));
                color: rgba(255, 255, 255, 210);
                border-radius: 5px;
            }
            QPushButton#buttonRegister:hover {
                background-color: qlineargradient(spread: pad, x1:0, y1:0.505682, x2:1, y2:0.477,
                                                  stop:0 rgba(40, 67, 98, 219), stop:1 rgba(105, 118, 132, 226));
            }
            QPushButton#buttonRegister:pressed {
                background-color: rgba(105, 118, 132, 200);
                padding-left: 5px;
                padding-top: 5px;
            }
        """

    def createSocialButtons(self):
        icons = [
            QDir.current().filePath("QLabel/Images/iconF.svg"),  # Facebook
            QDir.current().filePath("QLabel/Images/iconY.svg"),  # YouTube
            QDir.current().filePath("QLabel/Images/iconT.svg"),  # Twitter
            QDir.current().filePath("QLabel/Images/iconIn.svg")  # LinkedIn
        ]
        urls = [
            "https://www.facebook.com",  # URL của Facebook
            "https://www.youtube.com",  # URL của YouTube
            "https://www.twitter.com",  # URL của Twitter
            "https://www.linkedin.com"  # URL của LinkedIn
        ]
        x_positions = [115, 165, 215, 265]
        for x, iconPath, url in zip(x_positions, icons, urls):
            self.createSocialButton(x, 435, iconPath, url)

    def openSocialApp(self, url):
        QDesktopServices.openUrl(QUrl(url))

    def createSocialButton(self, x, y, iconPath, url):
        btn = QPushButton(self)
        btn.setGeometry(QRect(x, y, 40, 40))
        btn.setIcon(QIcon(iconPath))
        btn.setStyleSheet("""
            QPushButton{
                border-radius: 20px;
                background-color: rgba(105, 198, 207, 0.7);
                border: 1px solid rgba(185, 225, 207, 0.7);
            }
            QPushButton::hover{
                background-color: rgba(155, 248, 255, 0.7);
            }
            QPushButton::pressed{
                padding-left: 5px;
                padding-top: 5px;
                background-color: rgba(125, 218, 227, 0.7);
            }
        """)
        btn.clicked.connect(lambda: self.openSocialApp(url))

    def createExitButton(self):
        btnExit = QPushButton(self)
        btnExit.setGeometry(370, 30, 30, 30)
        btnExit.setIcon(QIcon(QDir.current().filePath("QLabel/Images/iconExit.svg")))
        btnExit.setStyleSheet("""
            QPushButton{
                border-top-right-radius: 20px;
                background-color: transparent;
            }
            QPushButton::hover{
                background-color: rgba(110, 141, 255, 0.7);
            }
            QPushButton::pressed{
                padding-left: 5px;
                padding-top: 5px;
            }
        """)
        btnExit.clicked.connect(self.closeApp)

    def closeApp(self):
        QApplication.quit()

    def center(self):
        screen = QApplication.primaryScreen()
        screenGeometry = screen.availableGeometry()
        screenWidth, screenHeight = screenGeometry.width(), screenGeometry.height()

        windowWidth, windowHeight = self.width(), self.height()
        x = (screenWidth - windowWidth) // 2
        y = (screenHeight - windowHeight) // 2

        self.move(x, y)