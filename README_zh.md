# [ForMaiR](https://formair.io) - auto Forward eMails with custom Rules

<p align="center">
    <a href="https://github.com/k8scat/ForMaiR">GitHub</a> |
    <a href="https://gitee.com/hsowan/ForMaiR">码云</a>
</p>

自定义规则的邮件自动转发工具。

## 使用

```bash
# 克隆代码仓
git clone git@gitee.com:hsowan/ForMaiR.git
cd ForMaiR

# 从 template/config.yaml 复制一份配置文件
cp template/config.yaml config.yaml

# 初始化 python3 的环境
virtualenv -p python3 .venv
source .venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 开始根据自定义的规则进行转发邮件
python main.py config.yaml
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
