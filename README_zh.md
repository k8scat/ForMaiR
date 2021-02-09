# [ForMaiR](https://formair.io) - auto Forward eMails with custom Rules

<p align="center">
  <a href="https://www.codefactor.io/repository/github/k8scat/formair"><img src="https://www.codefactor.io/repository/github/k8scat/formair/badge" alt="CodeFactor" /></a>
</p>

<p>
  <a href="https://github.com/k8scat/ForMaiR">GitHub</a> |
  <a href="https://gitee.com/hsowan/ForMaiR">码云</a>
</p>

自定义规则的邮件自动转发工具。

## 安装

### 使用 `pip`

```bash
$ python3 -m pip install --user formair
```

### 使用 `git`

```bash
$ git clone git@github.com:k8scat/ForMaiR.git
$ cd ForMaiR
$ python3 setup.py install
```

## 使用

参考配置：[template/config.yaml](https://github.com/k8scat/ForMaiR/blob/master/template/config.yaml)

```bash
$ formair # 从 ./config.yaml 中加载配置

$ formair /path/to/config.yaml # 从 /path/to/config.yaml 中加载配置
```

## 自定义规则

满足下列任一规则的邮件会被转发到指定的邮箱列表（`to_addrs`）

- [x] 邮件的发件人（`from_addr[1]`）在指定的发件人列表中（`from_addrs`）
- [x] 邮件的主题（`subject`）匹配指定的主题正则表达式（`subject_pattern`）
- [x] 邮件的内容（`plain_content` 或 `html_content`）匹配指定的内容正则表达式（`content_pattern`）

```yaml
rules:
  -
    to_addrs:
      - 't1@example.com'
      - 't2@example.com'
    from_addrs:
      - 'f1@example.com'
      - 'f2@example.com'
    subject_pattern: ''
    content_pattern: ''
  -
    to_addrs:
      - 't1@example.com'
      - 't2@example.com'
    from_addrs:
      - 'f1@example.com'
      - 'f2@example.com'
    subject_pattern: ''
    content_pattern: ''
```

## 只转发新邮件

支持转发指定范围内的新邮件。

- 从 _index_file_ 文件中获取上次读取的邮件位置（`last_email_index`） (如果文件不存在，则默认是 0)
- 从 `pop3_server.stat` 获取当前邮件的总数（`email_count`）

```python
for index in range(last_email_index+1, email_count+1):
    pass
```
