# [ForMaiR](https://formair.io) - auto Forward eMails with custom Rules

<p align="center">
  <a href="https://www.codefactor.io/repository/github/k8scat/formair"><img src="https://www.codefactor.io/repository/github/k8scat/formair/badge" alt="CodeFactor" /></a>
</p>

<p>
  <a href="https://github.com/k8scat/ForMaiR">GitHub</a> |
  <a href="https://gitee.com/hsowan/ForMaiR">码云</a>
</p>

## Installation

### Install using `pip`

```bash
$ python3 -m pip install --user formair
```

### Install using `git`

```bash
$ git clone git@github.com:k8scat/ForMaiR.git
$ cd ForMaiR
$ python3 setup.py install
```

## Usage

Refer config: [template/config.yaml](https://github.com/k8scat/ForMaiR/blob/master/template/config.yaml)

```bash
$ formair # load config from ./config.yaml

$ formair /path/to/config.yaml # load config from /path/to/config.yaml
```

## Custom rules

Emails which meet follow rules will be auto forwarded to `to_addrs`.

- [x] Email `from_addr[1]` in `from_addrs`
- [x] Email `subject` meet `subject_pattern`
- [x] Email `plain_content` or `html_content` meet `content_pattern`

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

## Only forwarding the new emails

Support forwarding new emails in the specified range.

- Get `last_email_index` from the _index_file_ (default 0 if not exists)
- Get `email_count` from `pop3_server.stat`

```python
for index in range(last_email_index+1, email_count+1):
    pass
```
