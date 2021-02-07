# ForMaiR - auto Forward eMails with custom Rules

<p align="center">
    <a href="https://github.com/k8scat/ForMaiR">GitHub</a> |
    <a href="https://gitee.com/hsowan/ForMaiR">码云</a>
</p>

自定义规则的邮件自动转发工具。

## 自定义规则

满足下列任一规则的邮件会被转发到指定的邮箱列表（`to_addrs`）

- [x] 邮件的发件人（`from_addr[1]`）在指定的发件人列表中（`from_addrs`）
- [x] 邮件的主题（`subject`）匹配指定的主题正则表达式（`subject_pattern`）
- [x] 邮件的内容（`plain_content` 或 `html_content`）匹配指定的内容正则表达式（`content_pattern`）

```python
email = {
    'from_addr': ('realname', 'noal@example.com'),
    'subject': '',
    'plain_content': '',
    'html_content': ''
}

transfer_rules = [
    {
        'to_addrs': [''],
        'from_addrs': [''],
        'subject_pattern': r'',
        'content_pattern': r''
    }
]
```

## 关于 `last_email_count`

`Cafe` 支持自动转发指定范围内的邮件。

```python
[last_email_count+1, email_count+1]
```

- `last_email_count` 从 `index_file` 文件中读取 (如果文件不存在，则默认是 0)
- `email_count` 从 `pop3_server.stat` 获取
