#FROM alpine:3.2
#RUN apk update && apk add --update-cache -t ansible python

FROM ubuntu:14.04

RUN DEBIAN_FRONTEND=noninteractive apt-get install -y software-properties-common \
    && apt-add-repository ppa:ansible/ansible \
    && DEBIAN_FRONTEND=noninteractive apt-get update \
    && DEBIAN_FRONTEND=noninteractive apt-get install -y ansible python python-simplejson

# workaround for Ansible <= 1.9.4
# see https://github.com/ansible/ansible-modules-core/pull/2258
RUN find . -type f -name "docker.py" -exec sed -i "s/image\['ContainerConfig'\]\['ExposedPorts'\]/image['ContainerConfig'].get('ExposedPorts')/g" {} +
RUN find . -type f -name "docker.py" -exec sed -i "s/container\[\"Config\"]\[\"ExposedPorts\"\]/container['Config'].get('ExposedPorts')/g" {} +

WORKDIR /ansible
ADD ./known_hosts /root/.ssh/known_hosts
ADD . /ansible

CMD ["ansible", "--version"]
