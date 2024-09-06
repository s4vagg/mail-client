# utils.py
import imaplib
import smtplib

def connect_imap(email, password):
    imap_server = "imap.yandex.ru"
    imap_port = 993
    imap_conn = imaplib.IMAP4_SSL(imap_server, imap_port)
    imap_conn.login(email, password)
    return imap_conn

def connect_smtp(email, password):
    smtp_server = "smtp.yandex.ru"
    smtp_port = 465
    smtp_conn = smtplib.SMTP_SSL(smtp_server, smtp_port)
    smtp_conn.login(email, password)
    return smtp_conn
