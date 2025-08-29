#!/usr/bin/python3

import smtplib
import yaml
from email.message import EmailMessage

smtp_config = yaml.safe_load(open('/home/asc/dev/asc-system/.config/smtp_config.yml'))
smtp_usr = smtp_config['smtp_usr']
smtp_pwd = smtp_config['smtp_pwd']
smtp_svr = smtplib.SMTP("smtp.office365.com", 587)

def connect_smtp():
    smtp_svr.ehlo()
    smtp_svr.starttls()
    smtp_svr.login(smtp_usr, smtp_pwd)

#Define funcitons and args
def send_email(recipient, subject, body):

    # try:
    #     smtp_server = None
    #     smtp_server = smtplib.SMTP("YOUR.MAIL.SERVER", 587)
    #     smtp_server.ehlo()
    #     smtp_server.starttls()
    #     smtp_server.ehlo()
    #     smtp_server.login("USERNAME@DOMAIN", password)
    #     smtp_server.send_message(message)
    # except Exception as e:
    #     print("Error: ", str(e))
    # finally:
    #     if smtp_server is not None:
    #         smtp_server.quit()



    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = 'asc.system@appliedstemcell.com'
    msg['To'] = recipient
    # msg['To'] = 'santiago.gomez@appliedstemcell.com'
    msg.set_content(body, subtype='html')
    smtp_svr.send_message(msg)
    return None

def disconnect_smtp():
    ##Close vs quit
    smtp_svr.close()


