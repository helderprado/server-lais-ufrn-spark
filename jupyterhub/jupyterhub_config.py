import os
from docker.types import Mount, DriverConfig
from pathlib import Path

# DOCKER IMAGE
notebook_image = os.environ['DOCKER_JUPYTER_IMAGE']
c.SwarmSpawner.image = notebook_image

# DEFAULT CONFIG
c.ConfigurableHTTPProxy.should_start = True
c.JupyterHub.authenticator_class = "dummy"
c.Spawner.default_url = '/lab'
c.JupyterHub.spawner_class = 'dockerspawner.SwarmSpawner'

# NETWORK
c.SwarmSpawner.network_name = os.environ['DOCKER_NETWORK_NAME']
c.SwarmSpawner.extra_host_config = {
    'network_mode': os.environ['DOCKER_NETWORK_NAME']}

# CONTAINERS
c.SwarmSpawner.remove_containers = True
c.SwarmSpawner.debug = True
c.JupyterHub.hub_ip = os.environ['HUB_IP']

# ENVIRONMENT
c.Spawner.env_keep = ['JUPYTER_ENABLE_LAB',
                      'PYSPARK_SUBMIT_ARGS',
                      'AWS_ACCESS_KEY_ID',
                      'AWS_SECRET_ACCESS_KEY',
                      'MLFLOW_S3_ENDPOINT_URL']

# Helper function for creating PyDocker Mount.


def nfs_mount(nfs_target, nfs_source, nfs_device, read_only=False):
    return Mount(
        type="volume",
        target=nfs_target,
        source=nfs_source,
        no_copy=True,
        read_only=read_only,
        driver_config=DriverConfig(
            name="local",
            options={
                "type": "nfs4",
                "o": f"addr=192.168.100.5, rw",
                "device": nfs_device,
            },
        ),
    )

# Called before spawning container, used for doing user specific settings.


def pre_spawn_hook(spawner):
    try:
        username = spawner.user.name.lower()  # get the login username
        spawner.log.info(f"pre_spawn_hook for {username}")

        # Change default user joyvan to the username.
        # spawner.environment["NB_USER"] = username

        spawner.extra_container_spec["mounts"] = [{"type": "volume",
                                                   "source": "server_nfs-data",
                                                   "target": f"/home/jovyan/shared",
                                                   "volume": {
                                                       "nocopy": True
                                                   }
                                                   }]

        # Make local user gain root priviliges so that we can change username/uid/gid later.
        spawner.extra_container_spec["user"] = "root"

    except Exception as e:
        spawner.log.error(e)

# Make sure mount points exist and return them to be used by DockerSpawner.
# nfs_server need to be specified !!!


# def _get_mount_points(spawner, username):
#     container_mounts = []
#     try:

#         # # Create user home directory if does not exist on nfs server.
#         # home_path = Path("shared") / username

#         # if not home_path.is_dir():
#         #     home_path.mkdir(0o755)  # local home folder permissions.

#         # # Create link to shared directory in users home directory if not already there on nfs server.
#         # shared_path = home_path / "shared"
#         # if not shared_path.is_symlink():
#         #     shared_path.symlink_to(Path("..") / "shared")

#         # Mounts for everyone:
#         # - /home/USERNAME/work       - contains your personal work.
#         # - /home/USERNAME/shared     - shared folder, will be read-only for normal users and read-write for admins.
#         # container_mounts.append(
#         #     nfs_mount("/work", f"jupyterhub_{username}", ":/home"))

#         container_mounts.append(
#             f"/home/{username}/shared", "jupyterhub_public_shared", f":/mnt")

#         spawner.log.info("DEU TUDO CERTO")

#     except Exception as e:
#         spawner.log.error("O erro foi: ", e)

#     return container_mounts


# START SPAWNER
c.Spawner.cmd = ["start-singleuser.sh"]
c.Spawner.pre_spawn_hook = pre_spawn_hook

c.SwarmSpawner.http_timeout = 300
c.SwarmSpawner.start_timeout = 300
