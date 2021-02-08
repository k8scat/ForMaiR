import smtplib
import logging
import time

from email.utils import parseaddr, COMMASPACE, formataddr
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class SMTP:
    server = None

    def __init__(self, host: str, user: str, password: str, port: int = 0,
                 enable_ssl: bool = True, real_name: str = ''):
        self.host = host
        self.user = user
        self.password = password
        self.port = port
        self.enable_ssl = enable_ssl
        self.real_name = real_name
        if not port:
            if self.enable_ssl:
                self.port = smtplib.SMTP_SSL_PORT
            else:
                self.port = smtplib.SMTP_PORT
                
    def login(self, max_login_retry: int = 3, login_interval: int = 10) -> None:
        self.server = smtplib.SMTP_SSL(self.host, self.port)
        # self.server.set_debuglevel(1)
        for count in range(max_login_retry):
            try:
                self.server.login(self.user, self.password)
                break
            except Exception as e:
                logging.warning('smtp server login failed: %s', e)
                if count == max_login_retry - 1:
                    raise 'cannot login smtp server'
                logging.info(
                    'try to login smtp server again in %ds', login_interval)
                time.sleep(login_interval)

    def send_email(self, to_addrs: list, subject: str = '',
                   plain_content: str = '', html_content: str = '',
                   attachments=None):
        assert isinstance(to_addrs, list)
        assert len(to_addrs) > 0
        assert len(subject) > 0

        msg = MIMEMultipart('alternative')
        msg['From'] = SMTP.format_addr(f'{self.real_name} <{self.user}>')
        msg['To'] = COMMASPACE.join(to_addrs)
        msg['Subject'] = Header(subject, 'utf-8').encode()

        msg.attach(MIMEText(plain_content, 'plain', 'utf-8'))

        if html_content != '':
            msg.attach(MIMEText(html_content, 'html', 'utf-8'))

        for attachment in attachments or []:
            msg.attach(attachment)

        try:
            self.server.sendmail(self.user, to_addrs, msg.as_string())
        except Exception as e:
            logging.error('send email failed: %s', e)

    @staticmethod
    def format_addr(s):
        name, addr = parseaddr(s)
        return formataddr((Header(name, 'utf-8').encode(), addr))    
