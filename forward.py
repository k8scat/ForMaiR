# -*- coding: utf-8 -*-
# Name: Cafe
# Author: K8sCat <k8scat@gmail.com>
# Function: Auto Forward Emails with Custom rules.

import poplib
import logging
import smtplib
import os
import re

from email.parser import Parser
from email.header import decode_header
from email.utils import parseaddr, COMMASPACE, formataddr
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.message import Message

cur_dir = os.path.dirname(__file__)
index_file = os.path.join(cur_dir, 'email_count.txt')

pop3_user = ''
pop3_password = ''
pop3_host = 'pop.qq.com'
pop3_ssl_port = 995

smtp_user = ''
smtp_password = ''
smtp_host = 'smtp.exmail.qq.com'
smtp_port = 465

pop3_resp_status_ok = b'+OK'

transfer_rules = [
    {
        'to_addrs': [''],
        'from_addrs': [''],
        'subject_pattern': r'',
        'content_pattern': r''
    }
]

logging.basicConfig(level=logging.INFO,
                    format="[%(levelname)s] %(asctime)s %(filename)s: %(message)s",
                    datefmt="%Y-%m-%d %H:%M:%S")


def get_pop3_ssl_server(host: str, port: int, user: str, password: str) -> poplib.POP3:
    poplib._MAXLINE = 1024 * 1024
    server = poplib.POP3_SSL(host=pop3_host, port=port)
    # server.set_debuglevel(1)
    server.user(pop3_user)
    server.pass_(pop3_password)
    return server


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


def decode_str(s: str) -> str:
    value, charset = decode_header(s)[0]
    if charset:
        value = value.decode(charset, errors='ignore')
    return value


def parse_email_header(msg: Message, header: str) -> tuple:
    value = msg.get(header, '')
    if value == '':
        return ('', '')

    assert header in ['Subject', 'From', 'To']
    if header == 'Subject':
        return decode_str(value)

    name, email = parseaddr(value)
    name = decode_str(name)
    return (name, email)


def parse_email_content(msg: Message) -> str:
    content = msg.get_payload(decode=True)
    charset = guess_charset(msg)
    if charset:
        content = content.decode(charset, errors='ignore')
    return content


def parse_email(msg: Message) -> dict:
    email = dict(
        subject=parse_email_header(msg, 'Subject'),
        from_addr=parse_email_header(msg, 'From'),
        to_addr=parse_email_header(msg, 'To'),
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
            email['plain_content'] = parse_email_content(part)
        elif content_type == 'text/html':
            email['html_content'] = parse_email_content(part)
        elif content_type == 'application/octet-stream':
            content_disposition = part.get('Content-Disposition', '')
            attachment = generate_attachment(
                part.get_payload(), content_disposition=content_disposition)
            email['attachments'].append(attachment)
        else:
            logging.info(f'ignore content_type: {content_type}')

    return email


def pop3_stat(server: poplib.POP3) -> int:
    email_count, total_size = server.stat()
    logging.info(f'emails count: {email_count}, total size: {total_size}')
    return email_count


def list_all_emails(server: poplib.POP3):
    # emails: [b'1 82923', b'2 2184', ...]
    resp, emails, _ = server.list()
    assert resp.startswith(pop3_resp_status_ok), f'get email failed: {resp}'
    return emails


def get_email(server: poplib.POP3, index: int) -> dict:
    resp, lines, octets = server.retr(index)
    assert resp.startswith(pop3_resp_status_ok), f'get email failed: {resp}'
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
            logging.warning(f'message charset not found so still use utf-8 but ignore errors')
            charset = 'utf-8'
        else:        
            logging.info(f'found message charset: {charset}')
        try:
            msg_content = b'\r\n'.join(lines).decode(charset, errors='ignore')
        except Exception as e:
            logging.error(f'decode message failed again: {e}')
            return None
            
    msg = Parser().parsestr(msg_content)  
    return parse_email(msg)


def forward_emails(start: int, end: int):
    for i in range(start, end):
        # 重新创建 pop3_server：server.retr 在使用同一个 pop3_server 的时候会出现 response doesn't start with '+' 的错误
        pop3_server = get_pop3_ssl_server(
            pop3_host, pop3_ssl_port, pop3_user, pop3_password)
        try:
            logging.info(f'new email: {i}')
            email = get_email(pop3_server, i)
            if email is None:
                continue
            
            logging.info(f'email: {email["subject"]} from {email["from_addr"]}')
            to_addrs = check_forward_rule(email)
            if len(to_addrs) > 0:
                send_email(to_addrs, email['subject'], email['plain_content'],
                           email['html_content'], email['attachments'])
        finally:
            pop3_server.close()


def check_forward_rule(email: dict) -> list:
    to_addrs = []
    from_addr = email['from_addr'][1]
    for rule in transfer_rules:
        subject_pattern = re.compile(
            rule['subject_pattern']) if rule['subject_pattern'] else None
        content_pattern = re.compile(
            rule['content_pattern']) if rule['content_pattern'] else None
        if (subject_pattern and subject_pattern.fullmatch(email['subject'])) \
            or (content_pattern and (content_pattern.fullmatch(email['plain_content']) \
                or content_pattern.fullmatch(email['html_content']))) \
            or from_addr in rule['from_addrs']:
            to_addrs.extend(rule['to_addrs'])
    return to_addrs


def format_addr(s: str) -> str:
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), addr))


def send_email(to_addrs, subject, plain_content='', html_content='', attachments=None):
    assert isinstance(to_addrs, list)

    msg = MIMEMultipart('alternative')
    msg['From'] = format_addr(f'AICoder <{smtp_user}>')
    msg['To'] = COMMASPACE.join(to_addrs)
    msg['Subject'] = Header(subject, 'utf-8').encode()

    msg.attach(MIMEText(plain_content, 'plain', 'utf-8'))

    if not html_content:
        html_content = plain_content
    msg.attach(MIMEText(html_content, 'html', 'utf-8'))

    for attachment in attachments or []:
        msg.attach(attachment)

    server = smtplib.SMTP_SSL(smtp_host, smtp_port)
    try:
        # server.set_debuglevel(1)
        server.login(smtp_user, smtp_password)
        logging.info(f'send email[{subject}] to {to_addrs}')
        # server.sendmail(smtp_user, to_addrs, msg.as_string())
    except Exception as e:
        logging.error(f'send email failed: {e}')
    finally:
        server.close()


def generate_attachment(content: bytes, filename: str = '', content_disposition: str = '') -> MIMEApplication:
    attachment = MIMEApplication(content, Name=filename)
    if content_disposition:
        attachment['Content-Disposition'] = content_disposition
    else:
        attachment.add_header('Content-Disposition',
                              'attachment', filename=filename)
    return attachment


def get_last_email_count():
    if not os.path.exists(index_file):
        return 0
    with open(index_file, 'r') as f:
        return int(f.read())


def update_email_count(count: int):
    with open(index_file, 'w') as f:
        f.write(str(count))


if __name__ == '__main__':
    pop3_server = get_pop3_ssl_server(
        pop3_host, pop3_ssl_port, pop3_user, pop3_password)
    try:
        email_count = pop3_stat(pop3_server)
        last_email_count = get_last_email_count()
        forward_emails(last_email_count+1, email_count+1)
        update_email_count(email_count)
    finally:
        pop3_server.close()
