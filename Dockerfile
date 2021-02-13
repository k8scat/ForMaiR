FROM python:3.6-alpine

LABEL maintainer="K8sCat <k8scat@gmail.com>"
LABEL version="1.3.0"

WORKDIR /formair

COPY . .

RUN python -m pip install --upgrade pip setuptools && \
pip install -r requirements.txt && \
python setup.py install

ENTRYPOINT [ "formair" ]
CMD [ "/formair/conf/config.yaml" ]