import libnfs
import os

notebook_image = os.environ['DOCKER_JUPYTER_IMAGE']
c.SwarmSpawner.image = notebook_image

c.ConfigurableHTTPProxy.should_start = True
c.JupyterHub.authenticator_class = "dummy"
c.Spawner.default_url = '/lab'
c.JupyterHub.spawner_class = 'dockerspawner.SwarmSpawner'
c.SwarmSpawner.network_name = os.environ['DOCKER_NETWORK_NAME']
c.SwarmSpawner.extra_host_config = {
    'network_mode': os.environ['DOCKER_NETWORK_NAME']}
#c.SwarmSpawner.extra_create_kwargs.update({'volume_driver': 'local'})
c.SwarmSpawner.remove_containers = True
c.SwarmSpawner.debug = True
c.JupyterHub.hub_ip = os.environ['HUB_IP']

c.Spawner.env_keep = ['JUPYTER_ENABLE_LAB',
                      'PYSPARK_SUBMIT_ARGS',
                      'AWS_ACCESS_KEY_ID',
                      'AWS_SECRET_ACCESS_KEY',
                      'MLFLOW_S3_ENDPOINT_URL']

spawn_cmd = os.environ.get('DOCKER_SPAWN_CMD', "start-singleuser.sh")
c.SwarmSpawner.cmd = spawn_cmd

notebook_dir = os.environ.get('DOCKER_NOTEBOOK_DIR') or '/home/jovyan/work'

# TLS config


#c.JupyterHub.ssl_key = os.environ['SSL_KEY']
#c.JupyterHub.ssl_cert = os.environ['SSL_CERT']

c.SwarmSpawner.http_timeout = 300
c.SwarmSpawner.start_timeout = 300

# notebook_dir = os.environ.get('DOCKER_NOTEBOOK_DIR') or '/home/jovyan/work'
# c.SwarmSpawner.notebook_dir = notebook_dir
# c.SwarmSpawner.volumes = {'jupyterhub-user-{username}': notebook_dir}

# c.JupyterHub.admin_access = True
# c.Authenticator.admin_users = {'helderprado'}
