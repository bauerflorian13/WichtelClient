import smtplib
from email.message import EmailMessage
from config import Config

class Mail(object):
    def __init__(self, config):
        self.fromaddr = config.mail_fromaddr

        self.server = smtplib.SMTP(config.mail_server, config.mail_port)
        self.server.ehlo()
        self.server.starttls()
        self.server.ehlo()
        self.server.login(config.mail_username, config.mail_password)
    
    def send_mail(self, toaddr, subject, content):
        msg = EmailMessage()
        msg.set_content(content)
        msg['Subject'] = subject
        msg['From'] = self.fromaddr
        msg['To'] = toaddr
        txt = msg.as_string()
        self.server.sendmail(self.fromaddr, toaddr, txt)
    
    def quit(self):
        self.server.quit()