#!/usr/bin/env python

import docker.client
import docker.utils
import os
import uuid
from urlparse import urlparse
from docker import Client as DockerClient

class DockerVolumeManager(object):

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

    def restore_volumes(self, container, source_file):
        details = self.client.inspect_container(container['name'])
        image = details['Image']

        volume_mappings = details['Volumes']
        volumes = volume_mappings.keys()

        def create_bind(volume_name,ro=False):
            return dict(bind=volume_name,ro=ro)

        binds = dict(zip(volume_mappings.values(), map(create_bind, volume_mappings.keys())))

        volumes.append('/backup')
        binds[os.path.dirname(source_file)] = create_bind('/backup', True)
        filename = os.path.basename(source_file)

        restore_command = 'sh -c "tar xfz /backup/{filename} --overwrite -C /"'.format(filename=filename)

        params = {
            'image':       image,
            'command':     restore_command,
            'volumes':     volumes,
            'host_config': docker.utils.create_host_config(binds=binds)
        }
        container = self.client.create_container(**params)
        response = self.client.start(container=container.get('Id'))
        self.client.wait(container=container.get('Id'))
        self.client.remove_container(container=container.get('Id'))

        return dict(
            params=params,
            volume_mappings=volume_mappings,
            binds=binds,
            filename=filename,
            container=container.get('Id'),
            response=response
        )

    def backup_volumes(self, container, target_dir):
        details = self.client.inspect_container(container['name'])
        image = details['Image']

        volume_mappings = details['Volumes']
        volumes = volume_mappings.keys()

        def create_bind(volume_name,ro=True):
            return dict(bind=volume_name,ro=ro)

        binds = dict(zip(volume_mappings.values(), map(create_bind, volume_mappings.keys())))

        volumes.append('/backup')
        binds[target_dir] = create_bind('/backup', False)
        filename = str(uuid.uuid4()) + '.tgz'

        backup_command = 'sh -c "tar cfz /backup/{filename} -C / {volumes}"'.format(filename=filename, volumes=' '.join(details['Volumes'].keys()))

        params = {
            'image':       image,
            'command':     backup_command,
            'volumes':     volumes,
            'host_config': docker.utils.create_host_config(binds=binds)
        }
        container = self.client.create_container(**params)
        response = self.client.start(container=container.get('Id'))
        self.client.wait(container=container.get('Id'))
        self.client.remove_container(container=container.get('Id'))

        backup_filename=os.path.expanduser(os.path.join(target_dir, filename))
        return dict(
            params=params,
            volume_mappings=volume_mappings,
            binds=binds,
            filename=backup_filename,
            container=container.get('Id'),
            response=response
        )

def main():
    module = AnsibleModule(
        argument_spec = dict(
            task        = dict(type='str', required=True),
            name        = dict(type='str', required=True),
            target_dir  = dict(type='str', required=False),
            source_file = dict(type='str', required=False)
        )
    )

    params = module.params

    manager = DockerVolumeManager(module)

    task = params['task']
    if task == 'backup':
        result = manager.backup_volumes(
            dict(name=params['name']),
            os.path.expanduser(params['target_dir']))
    elif task == 'restore':
        result = manager.restore_volumes(
            dict(name=params['name']),
            os.path.expanduser(params['source_file']))
    else:
        module.fail_json(msg='Unrecognized task %s. Must be one of: '
                             'backup; restore.' % task)

    module.exit_json(
        filename      = result['filename'],
        result        = result,
        ansible_facts = dict(filename=result['filename']),
        changed       = True
    )


from ansible.module_utils.basic import *

main()
