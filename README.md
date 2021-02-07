# ForMaiR - auto Forward eMails with custom Rules

<p align="center">
    <a href="https://github.com/k8scat/ForMaiR">GitHub</a> |
    <a href="https://gitee.com/hsowan/ForMaiR">码云</a>
</p>

## Custom rules

Emails which meet follow rules will be auto forwarded to `to_addrs`.

- [x] Email `from_addr[1]` in `from_addrs`
- [x] Email `subject` meet `subject_pattern`
- [x] Email `plain_content` or `html_content` meet `content_pattern`

```python
email = {
    'from_addr': ('realname', 'noal@example.com'),
    'subject': '',
    'plain_content': '',
    'html_content': ''
}

forward_rules = [
    {
        'to_addrs': [''],
        'from_addrs': [''],
        'subject_pattern': r'',
        'content_pattern': r''
    }
]
```

## About `last_email_count`

Support forward emails in the specified range.

```python
[last_email_count+1, email_count+1]
```

- `last_email_count` is read from the `index_file` (default 0 if not exists)
- `email_count` is from `pop3_server.stat`
