# Provisioning the gesellix.net servers via Ansible and Docker

## Ansible workflow/useful commands

### encrypt sensitive data with Ansible vault

    docker build -t gesellix.net .
    docker run --rm -it -v `pwd`:/proj -v ~/.gesellix_vault_pass.txt:/vault.key gesellix.net ansible-vault encrypt /proj/host_vars/gesellix.yml
    docker build -t gesellix.net .

### view Ansible vault encrypted data

    docker run --rm -it -v ~/.gesellix_vault_pass.txt:/vault.key gesellix.net ansible-vault view host_vars/gesellix.yml

### play a playbook

fully-fledged provisioning:

    docker run --rm -it -v ~/.gesellix_vault_pass.txt:/vault.key -v ~/.ssh/id_rsa:/root/.ssh/id_rsa gesellix.net ansible-playbook gesellix.yml --ask-sudo-pass --tags ""

reload only the proxy:

    docker run --rm -it -v ~/.gesellix_vault_pass.txt:/vault.key -v ~/.ssh/id_rsa:/root/.ssh/id_rsa gesellix.net ansible-playbook gesellix.yml --ask-sudo-pass --tags "proxy"

limited to a certain host:

    docker run --rm -it -v ~/.gesellix_vault_pass.txt:/vault.key -v ~/.ssh/id_rsa:/root/.ssh/id_rsa gesellix.net ansible-playbook gesellix.yml --ask-sudo-pass --tags "proxy" -l gesellix2

    docker run --rm -it -v ~/.gesellix_vault_pass.txt:/vault.key -v ~/.ssh/id_rsa:/root/.ssh/id_rsa gesellix.net ansible-playbook gesellix.yml --ask-sudo-pass --tags "ssh,users" -l gesellix2

    docker run --rm -it -v ~/.gesellix_vault_pass.txt:/vault.key -v ~/.ssh/id_rsa:/root/.ssh/id_rsa gesellix.net ansible-playbook gesellix.yml --ask-sudo-pass --tags "docker,keepass,proxy" -l gesellix2


### update `known_hosts`

    docker run -it --rm -v `pwd`/known_hosts:/root/.ssh/known_hosts -v ~/.gesellix_vault_pass.txt:/vault.key -v ~/.ssh/id_rsa:/root/.ssh/id_rsa gesellix.net ansible-playbook --ask-sudo-pass --tags=ssh gesellix.yml -l gesellix2
