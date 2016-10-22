# Provisioning the gesellix.net servers via Ansible and Docker

## Ansible workflow/useful commands

### encrypt sensitive data with Ansible vault

    docker build -t gesellix .
    docker run --rm -it -v `pwd`:/proj -v ~/.gesellix_vault_pass.txt:/vault.key gesellix ansible-vault encrypt /proj/host_vars/gesellix.yml
    docker build -t gesellix .

### view Ansible vault encrypted data

    docker run --rm -it -v ~/.gesellix_vault_pass.txt:/vault.key gesellix ansible-vault view host_vars/gesellix.yml

### play a playbook

fully-fledged provisioning:

    docker run --rm -it -v ~/.gesellix_vault_pass.txt:/vault.key -v ~/.ssh/id_rsa:/root/.ssh/id_rsa gesellix ansible-playbook gesellix.yml --ask-become-pass --tags ""

reload only the proxy:

    docker run --rm -it -v ~/.gesellix_vault_pass.txt:/vault.key -v ~/.ssh/id_rsa:/root/.ssh/id_rsa gesellix ansible-playbook gesellix.yml --ask-become-pass --tags "proxy"

limited to a certain host:

    docker run --rm -it -v ~/.gesellix_vault_pass.txt:/vault.key -v ~/.ssh/id_rsa:/root/.ssh/id_rsa gesellix ansible-playbook gesellix.yml --ask-become-pass --tags "proxy" -l gesellix2

    docker run --rm -it -v ~/.gesellix_vault_pass.txt:/vault.key -v ~/.ssh/id_rsa:/root/.ssh/id_rsa gesellix ansible-playbook gesellix.yml --ask-become-pass --tags "ssh,users" -l gesellix2

    docker run --rm -it -v ~/.gesellix_vault_pass.txt:/vault.key -v ~/.ssh/id_rsa:/root/.ssh/id_rsa gesellix ansible-playbook gesellix.yml --ask-become-pass --tags "docker,keepass,proxy" -l gesellix2


### update `known_hosts`

    # echo "" > `pwd`/known_hosts
    docker run -it --rm -v `pwd`/known_hosts:/root/.ssh/known_hosts -v ~/.gesellix_vault_pass.txt:/vault.key -v ~/.ssh/id_rsa:/root/.ssh/id_rsa gesellix ansible all -m ping
