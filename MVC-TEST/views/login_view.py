from PyQt6.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QGraphicsDropShadowEffect, QHBoxLayout
from PyQt6.QtGui import QFont, QColor, QIcon
from PyQt6.QtCore import QRect, QDir, Qt, QDesktopServices, QUrl, QStackedWidget, QApplication

class LoginView(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(1100, 200, 450, 550)
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
        self.label1 = QLabel(self)
        self.label1.setGeometry(30, 30, 370, 480)
        self.label1.setStyleSheet(f"border-image: url({QDir.current().filePath('QLabel/Images/background.jpg')});"
                             "border-radius: 20px;")
        self.label1.setScaledContents(True)
        self.label1.setGraphicsEffect(
            QGraphicsDropShadowEffect(blurRadius=25, xOffset=0, yOffset=0, color=QColor(234, 221, 186, 100)))

        self.label2 = QLabel(self)
        self.label2.setGeometry(30, 30, 370, 480)
        self.label2.setStyleSheet("background-color: qlineargradient(spread: pad, x1:0, y1:0, y2:0.715909, "
                             "stop:0 rgba(0, 0, 0, 9), stop:0.375 rgba(0, 0, 0, 50), "
                             "stop:0.835227 rgba(0, 0, 0, 75));"
                             "border-radius: 20px;")

        self.label3 = QLabel(self)
        self.label3.setGeometry(40, 60, 350, 450)
        self.label3.setStyleSheet("background-color: rgba(0, 0, 0, 75);"
                             "border-radius: 15px;")
        self.label3.setGraphicsEffect(
            QGraphicsDropShadowEffect(blurRadius=25, xOffset=0, yOffset=0, color=QColor(105, 221, 132, 100)))

        self.label4 = QLabel(self)
        self.label4.setGeometry(QRect(170, 90, 90, 45))
        self.label4.setFont(QFont("Times New Roman", 20, QFont.Weight.Bold))
        self.label4.setStyleSheet("color: rgba(255, 255, 255, 210);")
        self.label4.setText("Log In")

    def createLoginComponents(self):
        self.txtUser = self.createLineEdit(115, 160, " User Name", 10)
        self.txtPassword = self.createLineEdit(115, 240, " Password", 10, echoMode=QLineEdit.EchoMode.Password)

        self.labelNotice = QLabel(self)
        self.labelNotice.setGeometry(QRect(115, 200, 200, 45))
        self.labelNotice.setStyleSheet("color: red;")

        self.buttonLogIn = QPushButton(self)
        self.buttonLogIn.setGeometry(QRect(115, 310, 200, 45))
        self.buttonLogIn.setObjectName("buttonLogin")
        self.buttonLogIn.setStyleSheet(self.getLoginButtonStyle())
        self.buttonLogIn.setText("L o g I n")
        self.buttonLogIn.setFont(QFont("Times New Roman", 15, QFont.Weight.Bold))

        self.newUser(115, 355, "Forgot Password?", "Click Here")
        self.newUser(115, 385, "New User?", "Sign Up")

    def createLineEdit(self, x, y, placeholder, fontSize, echoMode=None):
        self.lineEdit = QLineEdit(self)
        self.lineEdit.setGeometry(QRect(x, y, 200, 30))
        self.lineEdit.setFont(QFont("Times New Roman", fontSize))
        self.lineEdit.setStyleSheet("background-color: rgba(0, 0, 0, 0);"
                               "border: none;"
                               "border-bottom: 2px solid rgba(155, 168, 182, 255);"
                               "color: rgba(255, 255, 255, 255);"
                               "padding-bottom: 7px;")
        self.lineEdit.setPlaceholderText(placeholder)
        if echoMode:
            self.lineEdit.setEchoMode(echoMode)
        return self.lineEdit

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
        for x, iconPath, self.url in zip(x_positions, icons, urls):
            self.createSocialButton(x, 435, iconPath, self.url)

    def openSocialApp(self, url):
        QDesktopServices.openUrl(QUrl(url))

    def createSocialButton(self, x, y, iconPath, url):
        self.btn = QPushButton(self)
        self.btn.setGeometry(QRect(x, y, 40, 40))
        self.btn.setIcon(QIcon(iconPath))
        self.btn.setStyleSheet("""
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

    def createExitButton(self):
        self.btnExit = QPushButton(self)
        self.btnExit.setGeometry(370, 30, 30, 30)
        self.btnExit.setIcon(QIcon(QDir.current().filePath("QLabel/Images/iconExit.svg")))
        self.btnExit.setStyleSheet("""
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
        self.btnExit.clicked.connect(self.closeApp)

    def closeApp(self):
        QApplication.quit()

    def newUser(self, x, y, txtFirst, txtSecond):
        self.parentWidget = QWidget(self)
        self.parentWidget.setGeometry(QRect(x, y, 200, 45))
        self.parentWidget.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        self.layout = QHBoxLayout(self.parentWidget)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(5)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.labelNewUser = QLabel(txtFirst, self.parentWidget)
        self.labelNewUser.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.labelNewUser.setStyleSheet("""
            QLabel {
                color: rgba(255, 255, 255, 140);
                background-color: transparent;
            }
        """)

        self.buttonSignUp = QPushButton(txtSecond, self.parentWidget)
        self.buttonSignUp.setStyleSheet("""
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

        self.layout.addWidget(self.labelNewUser)
        self.layout.addWidget(self.buttonSignUp)

        if txtSecond == "Sign Up":
            self.buttonSignUp.clicked.connect(self.register)

    def register(self):
        from views.register_view import RegisterView
        self.stacked_widget = QStackedWidget()
        self.stacked_widget.addWidget(self)
        self.stacked_widget.addWidget(RegisterView())
        self.registerWindow = RegisterView()
        self.registerWindow.show()

    def center(self):
        screen = QApplication.primaryScreen()
        screenGeometry = screen.availableGeometry()
        screenWidth, screenHeight = screenGeometry.width(), screenGeometry.height()

        windowWidth, windowHeight = self.width(), self.height()
        x = (screenWidth - windowWidth) // 2
        y = (screenHeight - windowHeight) // 2

        self.move(x, y)