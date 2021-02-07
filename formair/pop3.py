import poplib
import logging
import time

from email.parser import Parser
from email.header import decode_header
from email.message import Message
from email.utils import parseaddr
from formair.utils import generate_attachment


class POP3:
    poplib._MAXLINE = 1024 * 1024

    status_ok = b'+OK'
    server = None

    def __init__(self, host: str, user: str, password: str, port: int = 0, enable_ssl: bool = True,
                 max_login_retry: int = 3, login_interval: int = 10, debug_level: int = 0):
        self.host = host
        self.port = port
        self.enable_ssl = enable_ssl
        self.user = user
        self.password = password
        self.max_login_retry = max_login_retry
        self.login_interval = login_interval
        self.debug_level = debug_level
        if self.port is None:
            if self.enable_ssl:
                self.port = poplib.POP3_PORT
            else:
                self.port = poplib.POP3_SSL_PORT

    def login(self):
        self.server = poplib.POP3_SSL(host=self.host, port=self.port)
        self.server.set_debuglevel(self.debug_level)
        self.server.user(self.user)

        # pop3_server login retry: poplib.error_proto: b'-ERR login fail, please try again later'
        for count in range(self.max_login_retry):
            try:
                self.server.pass_(self.password)
                break
            except Exception as e:
                logging.warning(f'pop3 server login failed: {e}')
                if count == self.max_login_retry - 1:
                    raise 'cannot login pop3 server'
                logging.info(
                    f'try to login pop3 server again in {self.login_interval}s')
                time.sleep(self.login_interval)

    @staticmethod
    def guess_charset(msg: Message):
        charset = msg.get_charset()
        if charset is None:
            # text/plain; charset="utf-8"
            # text/plain; charset="utf-8"; format=flowed
            # text/plain; charset = "gbk"
            content_type = msg.get('Content-Type', '').lower().replace(' ', '')
            # print(content_type)
            for part in content_type.split(';'):
                if 'charset' in part:
                    pos = part.find('charset=')
                    charset = part[pos + 8:].strip()
                    break

        if charset is None:
            charset = 'utf-8'
        return charset

    @staticmethod
    def decode_str(s: str) -> str:
        value, charset = decode_header(s)[0]
        if charset:
            value = value.decode(charset, errors='ignore')
        return value

    @staticmethod
    def parse_email_header(msg: Message, header: str) -> tuple:
        value = msg.get(header, '')
        if value == '':
            return ('', '')

        assert header in ['Subject', 'From', 'To']
        if header == 'Subject':
            return POP3.decode_str(value)

        name, email = parseaddr(value)
        name = POP3.decode_str(name)
        return (name, email)

    @staticmethod
    def parse_email_content(msg: Message) -> str:
        content = msg.get_payload(decode=True)
        charset = POP3.guess_charset(msg)
        if charset:
            content = content.decode(charset, errors='ignore')
        return content

    @staticmethod
    def parse_email(msg: Message) -> dict:
        email = dict(
            subject=POP3.parse_email_header(msg, 'Subject'),
            from_addr=POP3.parse_email_header(msg, 'From'),
            to_addr=POP3.parse_email_header(msg, 'To'),
            plain_content='',
            html_content='',
            attachments=[]
        )

        parts = [msg]
        if msg.is_multipart():
            parts = msg.get_payload()
        for part in parts:
            content_type = part.get_content_type()
            if content_type == 'text/plain':
                email['plain_content'] = POP3.parse_email_content(part)
            elif content_type == 'text/html':
                email['html_content'] = POP3.parse_email_content(part)
            elif content_type == 'application/octet-stream':
                content_disposition = part.get('Content-Disposition', '')
                attachment = generate_attachment(
                    part.get_payload(), content_disposition=content_disposition)
                email['attachments'].append(attachment)
            else:
                logging.info(f'ignore content_type: {content_type}')

        return email

    def stat(self) -> int:
        email_count, total_size = self.server.stat()
        logging.info(f'emails count: {email_count}, total size: {total_size}')
        return email_count
        

    def list_all_emails(self):
        # emails: [b'1 82923', b'2 2184', ...]
        resp, emails, _ = self.server.list()
        assert resp.startswith(self.status_ok), f'get email failed: {resp}'
        return emails

    def get_email(self, index: int) -> dict:
        resp, lines, octets = self.server.retr(index)
        assert resp.startswith(self.status_ok), f'get email failed: {resp}'
        logging.info(f'email size: {octets}')

        # print(lines)
        # for line in lines:
        #     if b'Content-Type: ' in line:
        #         print(line)

        try:
            msg_content = b'\r\n'.join(lines).decode('utf-8')
        except Exception as e:
            logging.warning(f'decode message failed: {e}')
            logging.info('try to find message charset...')
            charset = ''
            for line in lines:
                if charset:
                    break
                if b'Content-Type: ' in line:
                    line = line.decode('utf-8').lower()
                    for part in line.split(';'):
                        if 'charset' in part:
                            pos = part.find('charset=')
                            charset = part[pos + 8:].strip()
                            break
            if charset == '':
                logging.warning(
                    f'message charset not found so still use utf-8 but ignore errors')
                charset = 'utf-8'
            else:
                logging.info(f'found message charset: {charset}')
            try:
                msg_content = b'\r\n'.join(lines).decode(
                    charset, errors='ignore')
            except Exception as e:
                logging.error(f'decode message failed again: {e}')
                return None

        msg = Parser().parsestr(msg_content)
        return POP3.parse_email(msg)
