# email_client.py
from PyQt5.QtWidgets import QMainWindow, QListWidget, QTextEdit, QVBoxLayout, QPushButton, QWidget, QSplitter
from PyQt5 import QtCore
import email
import imaplib

class EmailClientWindow(QMainWindow):
    def __init__(self, imap_connection, smtp_connection, email):
        super().__init__()
        self.imap_connection = imap_connection
        self.smtp_connection = smtp_connection
        self.email = email

        self.setWindowTitle("Email Client")
        self.setGeometry(100, 100, 800, 600)

        # Списки писем и область просмотра
        self.inbox_list = QListWidget()
        self.message_view = QTextEdit()
        self.message_view.setReadOnly(True)

        # Разделитель для списков и просмотра
        splitter = QSplitter(QtCore.Qt.Horizontal)
        splitter.addWidget(self.inbox_list)
        splitter.addWidget(self.message_view)

        # Кнопка для отправки нового письма
        self.compose_button = QPushButton("Compose New Email")
        self.compose_button.clicked.connect(self.compose_email)

        # Основной макет
        layout = QVBoxLayout()
        layout.addWidget(splitter)
        layout.addWidget(self.compose_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # Обработка события выбора письма
        self.inbox_list.itemClicked.connect(self.display_email)

        # Кнопка для загрузки писем
        self.load_button = QPushButton("Load Emails")
        self.load_button.clicked.connect(self.load_inbox)

        layout.addWidget(self.load_button)

    def load_inbox(self):
        self.inbox_list.clear()  # Очищаем список перед загрузкой новых сообщений
        self.imap_connection.select("inbox")
        result, data = self.imap_connection.search(None, "ALL")

        if result == "OK":
            for num in data[0].split():
                result, msg_data = self.imap_connection.fetch(num, "(RFC822)")
                if result == "OK":
                    msg = email.message_from_bytes(msg_data[0][1])
                    
                    # Попробуем получить заголовок "Subject"
                    subject = msg.get("Subject")
                    if subject:
                        decoded_subject = email.header.decode_header(subject)[0][0]
                        if isinstance(decoded_subject, bytes):
                            decoded_subject = decoded_subject.decode()
                    else:
                        decoded_subject = "No Subject"

                    # Добавляем заголовок в список
                    self.inbox_list.addItem(decoded_subject)

    def display_email(self, item):
        email_index = self.inbox_list.row(item) + 1
        result, msg_data = self.imap_connection.fetch(str(email_index), "(RFC822)")
        if result == "OK":
            msg = email.message_from_bytes(msg_data[0][1])
            for part in msg.walk():
                if part.get_content_type() == "text/plain":
                    self.message_view.setPlainText(part.get_payload(decode=True).decode())

    def compose_email(self):
        from compose_email_window import ComposeEmailWindow
        self.compose_window = ComposeEmailWindow(self.smtp_connection, self.email)
        self.compose_window.show()
