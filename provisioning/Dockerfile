FROM gesellix/ansible:2.1.0.0

WORKDIR /ansible
ADD ./known_hosts /root/.ssh/known_hosts
ADD . /ansible

CMD ["ansible", "--version"]
