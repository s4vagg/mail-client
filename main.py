# main.py
import sys
from PyQt5.QtWidgets import QApplication, QDialog, QMessageBox
from login_dialog import LoginDialog
from email_client import EmailClientWindow
from utils import connect_imap, connect_smtp

def main():
    app = QApplication(sys.argv)

    # Показать окно авторизации
    login_dialog = LoginDialog()
    if login_dialog.exec_() == QDialog.Accepted:
        email, password = login_dialog.get_credentials()

        try:
            # Подключение к серверам
            imap_conn = connect_imap(email, password)
            smtp_conn = connect_smtp(email, password)

            # Открыть главное окно клиента электронной почты
            main_window = EmailClientWindow(imap_conn, smtp_conn, email)
            main_window.show()

            sys.exit(app.exec_())
        except Exception as e:
            QMessageBox.critical(None, "Connection Error", f"Failed to connect: {e}")
            sys.exit(1)

if __name__ == "__main__":
    main()
