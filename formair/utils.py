import os
from email.mime.application import MIMEApplication

import yaml


def load_config(cfg_file: str) -> dict:
    # do not need set 'r' mode while open
    with open(cfg_file, encoding='utf-8') as f:
        return yaml.safe_load(f)


def get_last_email_index(index_file: str) -> int:
    if not os.path.exists(index_file):
        return 0
    with open(index_file, 'r') as f:
        return int(f.read())


def update_last_email_index(index_file: str, count: int):
    with open(index_file, 'w') as f:
        f.write(str(count))


def generate_attachment(content: bytes, filename: str = '',
                        content_disposition: str = '') -> MIMEApplication:
    attachment = MIMEApplication(content, Name=filename)
    if content_disposition:
        attachment['Content-Disposition'] = content_disposition
    else:
        attachment.add_header('Content-Disposition',
                              'attachment', filename=filename)
    return attachment
