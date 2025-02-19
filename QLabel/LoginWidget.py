from PyQt6.QtCore import Qt, QRect, QUrl, QDir
from PyQt6.QtWidgets import QLabel, QWidget, QApplication, QLineEdit, QGraphicsDropShadowEffect, QPushButton, QMessageBox, QHBoxLayout, QStackedWidget
from PyQt6.QtGui import QFont, QColor, QIcon, QDesktopServices
import sys
import MySQLdb as mdb

def QssLoader(file_path: str) -> str:
    with open(file_path, "r") as file:
        return file.read()

class Window(QWidget):
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
        self.label2.setObjectName("label2Background")
        self.label2.setGeometry(30, 30, 370, 480)
        self.label2.setStyleSheet(QssLoader(QDir.current().filePath("QLabel/styles.qss")))

        self.label3 = QLabel(self)
        self.label3.setObjectName("label3Background")
        self.label3.setGeometry(40, 60, 350, 450)
        self.label3.setStyleSheet(QssLoader(QDir.current().filePath("QLabel/styles.qss")))
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
        self.buttonLogIn.setStyleSheet(QssLoader(QDir.current().filePath("QLabel/styles.qss")))
        self.buttonLogIn.setText("L o g I n")
        self.buttonLogIn.setFont(QFont("Times New Roman", 15, QFont.Weight.Bold))
        self.buttonLogIn.clicked.connect(self.login)

        self.newUser(115, 355, "Forgot Password?", "Click Here")
        self.newUser(115, 385, "New User?", "Sign Up")

    def createLineEdit(self, x, y, placeholder, fontSize, echoMode=None):
        self.lineEdit = QLineEdit(self)
        self.lineEdit.setObjectName("lineEditLogin")
        self.lineEdit.setGeometry(QRect(x, y, 200, 30))
        self.lineEdit.setFont(QFont("Times New Roman", fontSize))
        self.lineEdit.setStyleSheet(QssLoader(QDir.current().filePath("QLabel/styles.qss")))
        self.lineEdit.setPlaceholderText(placeholder)
        if echoMode:
            self.lineEdit.setEchoMode(echoMode)
        return self.lineEdit

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
        self.btn = QPushButton(self)
        self.btn.setObjectName("btnSocial")
        self.btn.setGeometry(QRect(x, y, 40, 40))
        self.btn.setIcon(QIcon(iconPath))
        self.btn.setStyleSheet(QssLoader(QDir.current().filePath("QLabel/styles.qss")))
        self.btn.clicked.connect(lambda: self.openSocialApp(url))

    def createExitButton(self):
        self.btnExit = QPushButton(self)
        self.btnExit.setObjectName("btnExit")
        self.btnExit.setGeometry(370, 30, 30, 30)
        self.btnExit.setIcon(QIcon(QDir.current().filePath("QLabel/Images/iconExit.svg")))
        self.btnExit.setStyleSheet(QssLoader(QDir.current().filePath("QLabel/styles.qss")))
        self.btnExit.clicked.connect(self.closeApp)

    def closeApp(self):
        QApplication.quit()

    def login(self):
        u = self.txtUser.text()
        p = self.txtPassword.text()
        try:
            db = mdb.connect(host='localhost', user='root', passwd='', database='loginwidget')
            cursor = db.cursor()
            cursor.execute("SELECT * FROM user_list WHERE user=%s AND pass=%s", (u, p))
            result = cursor.fetchone()
            if result:
                self.labelNotice.setText("Login successful!")
            else:
                self.labelNotice.setText("Invalid Username or Password!")
        except mdb.Error as e:
            QMessageBox.critical(self, "Database Error", f"Error: {e}")
        finally:
            if db:
                db.close()

    def newUser(self, x, y, txtFirst, txtSecond):
        # Tạo một widget cha với kích thước cố định
        parentWidget = QWidget(self)
        parentWidget.setGeometry(QRect(x, y, 200, 45))
        # parentWidget.setStyleSheet("background-color: rgba(0, 0, 0, 50); border-radius: 5px;")
        parentWidget.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        # Sử dụng QVBoxLayout để căn giữa QLabel và QPushButton
        layout = QHBoxLayout(parentWidget) # type: ignore
        layout.setContentsMargins(0, 0, 0, 0)  # Loại bỏ padding giữa layout và widget
        layout.setSpacing(5)  # Khoảng cách giữa QLabel và 
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Căn giữa layout

        # Tạo QLabel
        self.labelNewUser = QLabel(txtFirst, parentWidget)
        self.labelNewUser.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Căn giữa text
        self.labelNewUser.setObjectName("labelNewUser")
        self.labelNewUser.setStyleSheet(QssLoader(QDir.current().filePath("QLabel/styles.qss")))

        # Tạo QPushButton
        self.buttonSignUp = QPushButton(txtSecond, parentWidget)
        self.buttonSignUp.setObjectName("btnTransferSignUp")
        self.buttonSignUp.setStyleSheet(QssLoader(QDir.current().filePath("QLabel/styles.qss")))

        # Thêm QLabel và QPushButton vào layout
        layout.addWidget(self.labelNewUser)
        layout.addWidget(self.buttonSignUp)

        if txtSecond == "Sign Up":
            self.buttonSignUp.clicked.connect(self.register)

    def register(self):
        from RegisterWidget import Window as rw
        self.stacked_widget = QStackedWidget()
        self.stacked_widget.addWidget(self)
        self.stacked_widget.addWidget(rw())
        self.registerWindow = rw()
        self.registerWindow.show()

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

# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     window = Window()
#     window.show()
#     sys.exit(app.exec())
