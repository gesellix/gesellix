#!/usr/bin/env python

import docker.client
import docker.utils
import os
from urlparse import urlparse
from docker import Client as DockerClient


class DockerFacts(object):
    def __init__(self, module):
        self.module = module
        self.client = self.create_docker_client(module)

    def create_docker_client(self, module):

        # Connect to the docker server using any configured host and TLS settings.

        env_host = os.getenv('DOCKER_HOST')
        env_docker_verify = os.getenv('DOCKER_TLS_VERIFY')
        env_cert_path = os.getenv('DOCKER_CERT_PATH')
        env_docker_hostname = os.getenv('DOCKER_TLS_HOSTNAME')

        docker_url = module.params.get('docker_url')
        if not docker_url:
            if env_host:
                docker_url = env_host
            else:
                docker_url = 'unix://var/run/docker.sock'

        tls_client_cert = module.params.get('tls_client_cert', None)
        if not tls_client_cert and env_cert_path:
            tls_client_cert = os.path.join(env_cert_path, 'cert.pem')

        tls_client_key = module.params.get('tls_client_key', None)
        if not tls_client_key and env_cert_path:
            tls_client_key = os.path.join(env_cert_path, 'key.pem')

        tls_ca_cert = module.params.get('tls_ca_cert')
        if not tls_ca_cert and env_cert_path:
            tls_ca_cert = os.path.join(env_cert_path, 'ca.pem')

        tls_hostname = module.params.get('tls_hostname')
        if tls_hostname is None:
            if env_docker_hostname:
                tls_hostname = env_docker_hostname
            else:
                parsed_url = urlparse(docker_url)
                if ':' in parsed_url.netloc:
                    tls_hostname = parsed_url.netloc[:parsed_url.netloc.rindex(':')]
                else:
                    tls_hostname = parsed_url
        if not tls_hostname:
            tls_hostname = True

        # use_tls can be one of four values:
        # no: Do not use tls
        # encrypt: Use tls.  We may do client auth.  We will not verify the server
        # verify: Use tls.  We may do client auth.  We will verify the server
        # None: Only use tls if the parameters for client auth were specified
        #   or tls_ca_cert (which requests verifying the server with
        #   a specific ca certificate)
        use_tls = module.params.get('use_tls')
        if use_tls is None and env_docker_verify is not None:
            use_tls = 'verify'

        tls_config = None
        if use_tls != 'no':
            params = {}

            # Setup client auth
            if tls_client_cert and tls_client_key:
                params['client_cert'] = (tls_client_cert, tls_client_key)

            # We're allowed to verify the connection to the server
            if use_tls == 'verify' or (use_tls is None and tls_ca_cert):
                if tls_ca_cert:
                    params['ca_cert'] = tls_ca_cert
                    params['verify'] = True
                    params['assert_hostname'] = tls_hostname
                else:
                    params['verify'] = True
                    params['assert_hostname'] = tls_hostname
            elif use_tls == 'encrypt':
                params['verify'] = False

            if params:
                # See https://github.com/docker/docker-py/blob/d39da11/docker/utils/utils.py#L279-L296
                docker_url = docker_url.replace('tcp://', 'https://')
                tls_config = docker.tls.TLSConfig(**params)

        return DockerClient(base_url=docker_url,
                            tls=tls_config)

    def list_existing_containes(self):
        params = {
            'all': True
        }
        containers = self.client.containers(**params)

        def extract_first_name(container):
            names = container.get('Names', [container.get('Id')])
            name = names[0].lstrip('/')
            return dict(name=name, container=container)

        containers_with_name = map(extract_first_name, containers)

        def name_as_key(acc, container):
            acc[container.get('name')] = container
            return acc

        containers_by_name = reduce(name_as_key, containers_with_name, {})

        return containers_by_name

    def inspect_container(self, name):
        params = {
            'container': name
        }
        container = self.client.inspect_container(**params)
        return container


def main():
    module = AnsibleModule(
        argument_spec=dict(
            name=dict(type='str', required=False, default=''),
        )
    )

    params = module.params

    name = params['name']

    docker_facts = DockerFacts(module)
    existing_containers = docker_facts.list_existing_containes()
    inspected_container = {}

    if name != '':
        inspected_container = docker_facts.inspect_container(name)

    module.exit_json(
        containers=existing_containers,
        inspected=inspected_container,
        ansible_facts=dict(
            containers=existing_containers,
            inspected=inspected_container),
        changed=False
    )


from ansible.module_utils.basic import *

main()
