"""
Name: ForMaiR - auto Forward eMails with custom Rules
Author: K8sCat <k8scat@gmail.com>
"""
import sys
import logging

from formair.forward import forward_emails
from formair.utils import load_config, get_last_email_index, update_last_email_index
from formair import pop3, smtp

logging.basicConfig(level=logging.INFO,
                    format="[%(levelname)s] %(asctime)s %(filename)s: %(message)s",
                    datefmt="%Y-%m-%d %H:%M:%S")

DEFAULT_INDEX_FILE = '.index'
DEFAULT_CONFIG_FILE = './config.yaml'


def init_pop3_server(config: dict) -> pop3.POP3:
    return pop3.POP3(host=config['host'], user=config['user'],
                     password=config['password'], port=config['port'],
                     enable_ssl=config['enable_ssl'])


def init_smtp_server(config: dict) -> smtp.SMTP:
    return smtp.SMTP(host=config['host'], user=config['user'],
                     password=config['password'], port=config['port'],
                     enable_ssl=config['enable_ssl'], real_name=config['real_name'])


def init_email_count(pop3_server: pop3.POP3) -> int:
    pop3_server.login()
    try:
        return pop3_server.stat()
    finally:
        if pop3_server.server:
            pop3_server.server.close()


def main():
    cfg_file = DEFAULT_CONFIG_FILE
    if len(sys.argv) == 2:
        cfg_file = sys.argv[1]
    config = load_config(cfg_file)
    index_file = config['index_file'] if config['index_file'] else DEFAULT_INDEX_FILE

    pop3_server = init_pop3_server(config['pop3'])
    email_count = init_email_count(pop3_server)

    smtp_server = init_smtp_server(config['smtp'])

    last_email_index = get_last_email_index(index_file)

    result = forward_emails(pop3_server, smtp_server,
                            last_email_index+1, email_count+1, rules=config['rules'])
    update_last_email_index(index_file, result)


if __name__ == '__main__':
    main()
