import logging
import os
import re

from formair import pop3, smtp

cur_dir = os.path.dirname(__file__)
index_file = os.path.join(cur_dir, 'email_count.txt')


smtp_host = ''
smtp_port = 465


def forward_emails(pop3_server: pop3.POP3, smtp_server: smtp.SMTP, start: int, end: int, rules: list) -> int:
    index = start
    try:
        for index in range(start, end):
            pop3_server.login()
            try:
                logging.info(f'email index: {index}')
                email = pop3_server.get_email(index)
                if email is None:
                    continue
                logging.info(f'get email {email["subject"]} from {email["from_addr"]}')
                to_addrs = _get_toaddrs_by_rules(rules, email)
                if len(to_addrs) > 0:
                    smtp_server.send_email(to_addrs, email['subject'], email['plain_content'],
                            email['html_content'], email['attachments'])
            finally:
                pop3_server.server.close()
    except Exception as e:
        logging.error(f'forward email failed: {e}')
    finally:
        return index - 1


def _get_toaddrs_by_rules(rules: list, email: dict) -> list:
    to_addrs = []
    from_addr = email['from_addr'][1]
    for rule in rules:
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
