## rebuild ansible image

    docker build -t gesellix.net .

## perform complete provisioning

    docker run --rm -it -v ~/.ssh/id_rsa:/root/.ssh/id_rsa gesellix.net ansible-playbook gesellix.yml --ask-sudo-pass --tags ""

## reload only the proxy

    docker run --rm -it -v ~/.ssh/id_rsa:/root/.ssh/id_rsa gesellix.net ansible-playbook gesellix.yml --ask-sudo-pass --tags "proxy"
