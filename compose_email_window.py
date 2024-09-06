# compose_email_window.py
from tkinter import messagebox
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QLineEdit, QTextEdit, QPushButton, QWidget, QLabel
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

class ComposeEmailWindow(QMainWindow):
    def __init__(self, smtp_connection, sender_email):
        super().__init__()
        self.smtp_connection = smtp_connection
        self.sender_email = sender_email

        self.setWindowTitle("Compose Email")
        self.setGeometry(200, 200, 600, 400)

        # Ввод получателя
        self.recipient_label = QLabel("Recipient:")
        self.recipient_input = QLineEdit()

        # Ввод темы
        self.subject_label = QLabel("Subject:")
        self.subject_input = QLineEdit()

        # Ввод текста письма
        self.message_label = QLabel("Message:")
        self.message_input = QTextEdit()

        # Кнопка отправки
        self.send_button = QPushButton("Send Email")
        self.send_button.clicked.connect(self.send_email)

        # Макет
        layout = QVBoxLayout()
        layout.addWidget(self.recipient_label)
        layout.addWidget(self.recipient_input)
        layout.addWidget(self.subject_label)
        layout.addWidget(self.subject_input)
        layout.addWidget(self.message_label)
        layout.addWidget(self.message_input)
        layout.addWidget(self.send_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def send_email(self):
        recipient_email = self.recipient_input.text()
        subject = self.subject_input.text()
        message = self.message_input.toPlainText()

        try:
            msg = MIMEMultipart()
            msg['From'] = self.sender_email
            msg['To'] = recipient_email
            msg['Subject'] = subject
            msg.attach(MIMEText(message, 'plain'))

            self.smtp_connection.sendmail(self.sender_email, recipient_email, msg.as_string())
            messagebox.information(self, "Success", "Email sent successfully!")
        except Exception as e:
            messagebox.critical(self, "Failed", f"Failed to send email: {e}")
