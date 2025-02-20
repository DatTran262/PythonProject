from PyQt6.QtWidgets import QApplication
from controllers.main_controller import MainController

def main():
    app = QApplication([])
    controller = MainController()
    controller.show_main_view()
    app.exec()

if __name__ == "__main__":
    main()