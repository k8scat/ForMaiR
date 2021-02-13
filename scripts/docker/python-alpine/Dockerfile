FROM python:3.6-alpine

LABEL maintainer="K8sCat <k8scat@gmail.com>"

# 使用阿里源
RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.aliyun.com/g' /etc/apk/repositories

# 安装 gcc: https://wiki.alpinelinux.org/wiki/GCC
# 安装 libffi-dev: https://github.com/jfloff/alpine-python/issues/44
RUN apk add build-base libffi-dev

RUN pip config set global.index-url https://mirrors.aliyun.com/pypi/simple && \
pip config set global.trusted-host mirrors.aliyun.com && \
python -m pip install --upgrade pip
