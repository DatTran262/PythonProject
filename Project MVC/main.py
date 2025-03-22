from PyQt6.QtWidgets import QApplication
from view import mv

def main():
    # Khởi tạo ứng dụng PyQt
    app = QApplication([])
    
    # Hiển thị cửa sổ chính
    window = mv()
    window.show()

    # Chạy Controller
    controller.run()

    # Chạy event loop của PyQt
    app.exec()

if __name__ == "__main__":
    main()
