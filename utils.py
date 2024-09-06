# utils.py
import imaplib
import smtplib
from email.mime.text import MIMEText

def connect_imap(email, password):
    conn = imaplib.IMAP4_SSL("imap.yandex.ru", 993)
    conn.login(email, password)
    return conn

def connect_smtp(email, password, smtp_server="smtp.yandex.ru"):
    conn = smtplib.SMTP_SSL(smtp_server, 465)
    conn.login(email, password)
    return conn
