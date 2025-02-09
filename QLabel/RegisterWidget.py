from PyQt6.QtCore import Qt, QRect, QUrl, QDir
from PyQt6.QtWidgets import QLabel, QWidget, QApplication, QLineEdit, QGraphicsDropShadowEffect, QPushButton, QMessageBox
from PyQt6.QtGui import QFont, QColor, QIcon, QDesktopServices
import sys
import MySQLdb as mdb


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
        label1 = QLabel(self)
        label1.setGeometry(30, 30, 370, 480)
        label1.setStyleSheet(f"border-image: url({QDir.current().filePath("QLabel/Images/background.jpg")});"
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

        buttonRegister = QPushButton(self)
        buttonRegister.setGeometry(QRect(115, 350, 200, 45))
        buttonRegister.setObjectName("buttonRegister")
        buttonRegister.setStyleSheet(self.getRegisterButtonStyle())
        buttonRegister.setText("R e g i s t e r")
        buttonRegister.setFont(QFont("Times New Roman", 15, QFont.Weight.Bold))
        buttonRegister.clicked.connect(self.register)

        btnSigIn = QPushButton("S i g n I n?",self)
        btnSigIn.setGeometry(QRect(180, 405, 70, 20))
        btnSigIn.setStyleSheet("""
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
        btnSigIn.clicked.connect(self.signin)

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
            db = mdb.connect(host='localhost', user='root', passwd='', database='loginwidget')
            cursor = db.cursor()
            
            # Kiểm tra xem username đã tồn tại chưa
            cursor.execute("SELECT * FROM user_list WHERE user=%s", (u,))
            if cursor.fetchone():
                self.labelNotice.setText("Username already exists!")
            else:
                # Thêm người dùng mới vào cơ sở dữ liệu
                cursor.execute("INSERT INTO user_list (user, pass) VALUES (%s, %s)", (u, p))
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
        from LoginWidget import Window as lw
        self.lw = lw()
        self.lw.show()

# app = QApplication(sys.argv)
# window = Window()
# window.show()
# sys.exit(app.exec())
