from PyQt6.QtCore import Qt, QRect, QUrl
from PyQt6.QtWidgets import QLabel, QLineEdit, QPushButton, QGraphicsDropShadowEffect, QMessageBox, QApplication
from PyQt6.QtGui import QFont, QColor, QDesktopServices, QIcon

class LoginView(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setGeometry(1500, 200, 450, 550)
        self.setWindowTitle("LogIn")
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        self.initUI()
        self.center()

    def initUI(self):
        self.createBackgroundLabels()
        self.createLoginComponents()
        self.createSocialButtons()
        self.createExitButton()

    def createBackgroundLabels(self):
        label1 = QLabel(self)
        label1.setGeometry(30, 30, 370, 480)
        label1.setStyleSheet("border-image: url(D:/Code/PyCharm/PythonProject/Images/background.jpg);"
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
        label4.setGeometry(QRect(170, 90, 90, 45))
        label4.setFont(QFont("Times New Roman", 20, QFont.Weight.Bold))
        label4.setStyleSheet("color: rgba(255, 255, 255, 210);")
        label4.setText("Log In")

    def createLoginComponents(self):
        self.txtUser = self.createLineEdit(115, 180, " User Name", 10)
        self.txtPassword = self.createLineEdit(115, 260, " Password", 10, echoMode=QLineEdit.EchoMode.Password)

        self.labelNotice = QLabel(self)
        self.labelNotice.setGeometry(QRect(115, 290, 200, 45))
        self.labelNotice.setStyleSheet("color: red;")

        self.buttonLogIn = QPushButton(self)
        self.buttonLogIn.setObjectName("buttonLogin")
        self.buttonLogIn.setStyleSheet(self.getLoginButtonStyle())
        self.buttonLogIn.setText("L o g I n")
        self.buttonLogIn.setGeometry(QRect(115, 340, 200, 45))
        self.buttonLogIn.setFont(QFont("Times New Roman", 15, QFont.Weight.Bold))

        label5 = QLabel(self)
        label5.setGeometry(QRect(115, 385, 200, 45))
        label5.setText("Forgot your User Name or Password?")
        label5.setStyleSheet("""
            color: rgba(255, 255, 255, 140);
        """)
        label5.setAlignment(Qt.AlignmentFlag.AlignCenter)

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

    def getLoginButtonStyle(self):
        return """
            QPushButton#buttonLogin {
                background-color: qlineargradient(spread: pad, x1:0, y1:0.505682, x2:1, y2:0.477,
                                                  stop:0 rgba(20, 47, 78, 219), stop:1 rgba(85, 98, 112, 226));
                color: rgba(255, 255, 255, 210);
                border-radius: 5px;
            }
            QPushButton#buttonLogin:hover {
                background-color: qlineargradient(spread: pad, x1:0, y1:0.505682, x2:1, y2:0.477,
                                                  stop:0 rgba(40, 67, 98, 219), stop:1 rgba(105, 118, 132, 226));
            }
            QPushButton#buttonLogin:pressed {
                background-color: rgba(105, 118, 132, 200);
                padding-left: 5px;
                padding-top: 5px;
            }
        """

    def show_error(self, message):
        QMessageBox.critical(self, "Error", message)

    def createSocialButtons(self):
        icons = [
            "D:/Code/PyCharm/PythonProject/Images/iconF.svg",  # Facebook
            "D:/Code/PyCharm/PythonProject/Images/iconY.svg",  # YouTube
            "D:/Code/PyCharm/PythonProject/Images/iconT.svg",  # Twitter
            "D:/Code/PyCharm/PythonProject/Images/iconIn.svg"  # LinkedIn
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
        btnExit.setIcon(QIcon("D:/Code/PyCharm/PythonProject/Images/iconExit.svg"))
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
        # Lấy kích thước của màn hình
        screen = QApplication.primaryScreen()
        screenGeometry = screen.availableGeometry()
        screenWidth, screenHeight = screenGeometry.width(), screenGeometry.height()

        # Tính toán vị trí căn giữa cửa sổ
        windowWidth, windowHeight = self.width(), self.height()
        x = (screenWidth - windowWidth) // 2
        y = (screenHeight - windowHeight) // 2

        # Di chuyển cửa sổ tới vị trí đã tính
        self.move(x, y)