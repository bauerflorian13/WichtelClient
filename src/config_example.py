class Config(object):
    def __init__(self):
        self.mail_server = 'mail.example.org'
        self.mail_port = 587
        self.mail_username = 'example@example.org'
        self.mail_password = 'examplepassword'
        self.mail_fromaddr = 'example@example.org'
        self.mail_enabled = False
        self.mail_subject = "Example Subject"