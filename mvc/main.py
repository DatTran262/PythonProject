import sys
import os

# Thêm thư mục gốc của dự án vào sys.path để có thể import module con
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from view.MainView import App as Window


def main():
    view = Window()
    view.show()


from PyQt6.QtWidgets import QApplication

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main()
    sys.exit(app.exec())
