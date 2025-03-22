from PyQt6.QtCore import Qt, QRect, QUrl, QDir
from PyQt6.QtWidgets import (
    QLabel,
    QWidget,
    QApplication,
    QLineEdit,
    QGraphicsDropShadowEffect,
    QPushButton,
    QMessageBox,
)
from PyQt6.QtGui import QFont, QColor, QIcon, QDesktopServices
import MySQLdb as mdb


def QssLoader(file_path: str) -> str:
    with open(file_path, "r") as file:
        return file.read()


class Window(QWidget):
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
        self.label1 = QLabel(self)
        self.label1.setGeometry(30, 30, 370, 480)
        self.label1.setStyleSheet(
            f"border-image: url({QDir.current().filePath("resources/Images/background.jpg")});"
            "border-radius: 20px;"
        )
        self.label1.setScaledContents(True)
        self.label1.setGraphicsEffect(
            QGraphicsDropShadowEffect(
                blurRadius=25, xOffset=0, yOffset=0, color=QColor(234, 221, 186, 100)
            )
        )

        self.label2 = QLabel(self)
        self.label2.setObjectName("label2Background")
        self.label2.setGeometry(30, 30, 370, 480)
        print(QssLoader(QDir.current().filePath("resources/Styles/styles.qss")))
        self.label2.setStyleSheet(QssLoader(QDir.current().filePath("resources/Styles/styles.qss")))

        self.label3 = QLabel(self)
        self.label3.setObjectName("label3Background")
        self.label3.setGeometry(40, 60, 350, 450)
        self.label3.setStyleSheet(QssLoader(QDir.current().filePath("resources/Styles/styles.qss")))
        self.label3.setGraphicsEffect(
            QGraphicsDropShadowEffect(
                blurRadius=25, xOffset=0, yOffset=0, color=QColor(105, 221, 132, 100)
            )
        )

        self.label4 = QLabel(self)
        self.label4.setGeometry(QRect(165, 90, 100, 45))
        self.label4.setFont(QFont("Times New Roman", 20, QFont.Weight.Bold))
        self.label4.setStyleSheet("color: rgba(255, 255, 255, 210);")
        self.label4.setText("Register")

    def createRegisterComponents(self):
        self.txtUser = self.createLineEdit(115, 160, " Email Address or Phone", 10)
        self.txtPassword = self.createLineEdit(
            115, 225, " Password", 10, echoMode=QLineEdit.EchoMode.Password
        )
        self.txtConfirmPassword = self.createLineEdit(
            115, 290, " Confirm Password", 10, echoMode=QLineEdit.EchoMode.Password
        )

        self.labelNotice = QLabel(self)
        self.labelNotice.setGeometry(QRect(115, 310, 200, 45))
        self.labelNotice.setStyleSheet("color: red;")

        self.buttonRegister = QPushButton(self)
        self.buttonRegister.setGeometry(QRect(115, 350, 200, 45))
        self.buttonRegister.setObjectName("buttonLogin")
        self.buttonRegister.setStyleSheet(
            QssLoader(QDir.current().filePath("resources/Styles/styles.qss"))
        )
        self.buttonRegister.setText("R e g i s t e r")
        self.buttonRegister.setFont(QFont("Times New Roman", 15, QFont.Weight.Bold))
        self.buttonRegister.clicked.connect(self.register)

        self.btnSigIn = QPushButton("S i g n I n?", self)
        self.btnSigIn.setObjectName("btnTransferSignUp")
        self.btnSigIn.setGeometry(QRect(180, 405, 70, 20))
        self.btnSigIn.setStyleSheet(QssLoader(QDir.current().filePath("resources/Styles/styles.qss")))
        self.btnSigIn.clicked.connect(self.signin)

    def createLineEdit(self, x, y, placeholder, fontSize, echoMode=None):
        self.lineEdit = QLineEdit(self)
        self.lineEdit.setObjectName("lineEditLogin")
        self.lineEdit.setGeometry(QRect(x, y, 200, 30))
        self.lineEdit.setFont(QFont("Times New Roman", fontSize))
        self.lineEdit.setStyleSheet(QssLoader(QDir.current().filePath("resources/Styles/styles.qss")))
        self.lineEdit.setPlaceholderText(placeholder)
        if echoMode:
            self.lineEdit.setEchoMode(echoMode)
        return self.lineEdit

    def createSocialButtons(self):
        icons = [
            QDir.current().filePath("resources/Images/iconF.svg"),  # Facebook
            QDir.current().filePath("resources/Images/iconY.svg"),  # YouTube
            QDir.current().filePath("resources/Images/iconT.svg"),  # Twitter
            QDir.current().filePath("resources/Images/iconIn.svg"),  # LinkedIn
        ]
        urls = [
            "https://www.facebook.com",  # URL của Facebook
            "https://www.youtube.com",  # URL của YouTube
            "https://www.twitter.com",  # URL của Twitter
            "https://www.linkedin.com",  # URL của LinkedIn
        ]
        x_positions = [115, 165, 215, 265]
        for x, iconPath, url in zip(x_positions, icons, urls):
            self.createSocialButton(x, 435, iconPath, url)

    def openSocialApp(self, url):
        QDesktopServices.openUrl(QUrl(url))

    def createSocialButton(self, x, y, iconPath, url):
        self.btn = QPushButton(self)
        self.btn.setObjectName("btnSocial2")
        self.btn.setGeometry(QRect(x, y, 40, 40))
        self.btn.setIcon(QIcon(iconPath))
        self.btn.setStyleSheet(QssLoader(QDir.current().filePath("resources/Styles/styles.qss")))
        self.btn.clicked.connect(lambda: self.openSocialApp(url))

    def createExitButton(self):
        self.btnExit = QPushButton(self)
        self.btnExit.setObjectName("btnExit")
        self.btnExit.setGeometry(370, 30, 30, 30)
        self.btnExit.setIcon(QIcon(QDir.current().filePath("resources/Images/iconExit.svg")))
        self.btnExit.setStyleSheet(QssLoader(QDir.current().filePath("resources/Styles/styles.qss")))
        self.btnExit.clicked.connect(self.closeApp)

    def closeApp(self):
        QApplication.quit()

    def register(self):
        u = self.txtUser.text()
        p = self.txtPassword.text()
        cp = self.txtConfirmPassword.text()

        # Kiểm tra xem các trường có rỗng không
        if not u or not p or not cp:
            self.labelNotice.setText("All fields are required!")
            return

        # Kiểm tra mật khẩu có khớp không
        if p != cp:
            self.labelNotice.setText("Passwords do not match!")
            return

        try:
            # Kết nối đến cơ sở dữ liệu
            db = mdb.connect(
                host="localhost", user="root", passwd="", database="loginwidget"
            )
            cursor = db.cursor()

            # Kiểm tra xem username đã tồn tại chưa
            cursor.execute("SELECT * FROM user_list WHERE user=%s", (u,))
            if cursor.fetchone():
                self.labelNotice.setText("Username already exists!")
            else:
                # Thêm người dùng mới vào cơ sở dữ liệu
                cursor.execute(
                    "INSERT INTO user_list (user, pass) VALUES (%s, %s)", (u, p)
                )
                db.commit()
                self.labelNotice.setText("Registration successful!")
        except mdb.Error as e:
            QMessageBox.critical(self, "Database Error", f"Error: {e}")
        finally:
            if db:
                db.close()

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

    def signin(self):
        self.close()
        from LoginView import Window as lv

        self.lv = lv()
        self.lv.show()


# import sys
# app = QApplication(sys.argv)
# window = Window()
# window.show()
# sys.exit(app.exec())
