# main.py
import sys
from PyQt5.QtWidgets import QApplication
from main_window import MainWindow
from email_client import EmailClientWindow


def main():
    app = QApplication(sys.argv)

    # Показать окно авторизации
    main_window = MainWindow()
    main_window.show()

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
