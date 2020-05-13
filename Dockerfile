FROM amazon/aws-cli:latest

COPY . .
COPY .docker/entrypoint.sh /entrypoint.sh

RUN yum install -y gettext python3 python3-pip && \
    pip3 install -r requirements.txt && \
    chmod u+x /entrypoint.sh

ENTRYPOINT ["/bin/sh", "/entrypoint.sh"]
