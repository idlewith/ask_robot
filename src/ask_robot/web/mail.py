# encoding: utf-8
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def send_email(title, content):
    email_from = os.getenv("email_from")
    password = os.getenv("email_password")
    email_to = os.getenv("email_to").split(",")

    content_template = f'<html> <head> <meta charset="utf-8"> <style> .body {{ font-family: "Microsoft YaHei" ! important; }} </style> </head> <body style="font-size: xx-large"> {content} </body> </html>'

    msg = MIMEMultipart()
    msg.attach(MIMEText(content_template, "html", "utf-8"))

    msg["Subject"] = "%s" % str(title)
    msg["From"] = email_from
    s = smtplib.SMTP_SSL("smtp.qq.com", 465)
    s.login(email_from, password)
    s.sendmail(email_from, email_to, msg.as_string())

