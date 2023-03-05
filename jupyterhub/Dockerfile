# Do not forget to pin down the version
FROM jupyterhub/jupyterhub:latest

# Copy the JupyterHub configuration in the container
COPY jupyterhub_config.py /srv/jupyterhub/jupyterhub_config.py

# # Download script to automatically stop idle single-user servers
# RUN wget https://raw.githubusercontent.com/jupyterhub/jupyterhub/1.2.1/examples/cull-idle/cull_idle_servers.py

# Install dependencies (for advanced authentication and spawning)
RUN pip install \
    dockerspawner==0.10.0 \
    oauthenticator==0.8.0 \
    jupyterhub-dummyauthenticator