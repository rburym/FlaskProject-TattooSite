import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from config import EMAIL_FROM, EMAIL_PAS

def get_msg(to: str, subject: str):
    msg = MIMEMultipart()
    msg['From'] = EMAIL_FROM
    msg['To'] = to
    msg['Subject'] = subject
    return msg


def send_email(message: str, to: str, subject: str, type_: str = 'plain'):
    msg = get_msg(to, subject)
    msg.attach(MIMEText(message, type_))
    server = smtplib.SMTP('smtp.yandex.ru', 587)
    server.starttls()
    server.login(EMAIL_FROM, EMAIL_PAS)
    server.sendmail(EMAIL_FROM, msg['To'], msg.as_string())
    server.quit()


