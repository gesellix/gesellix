#FROM alpine:3.2
#RUN apk update && apk add --update-cache -t ansible python

FROM gesellix/ansible:1.9.4

WORKDIR /ansible
ADD ./known_hosts /root/.ssh/known_hosts
ADD . /ansible

CMD ["ansible", "--version"]
