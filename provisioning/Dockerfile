#FROM alpine:3.2
#RUN apk update && apk add --update-cache -t ansible python

FROM ubuntu:14.04

RUN DEBIAN_FRONTEND=noninteractive apt-get install -y software-properties-common \
    && apt-add-repository ppa:ansible/ansible \
    && DEBIAN_FRONTEND=noninteractive apt-get update \
    && DEBIAN_FRONTEND=noninteractive apt-get install -y ansible python python-simplejson

WORKDIR /ansible
ADD . /ansible

CMD ["ansible", "--version"]
