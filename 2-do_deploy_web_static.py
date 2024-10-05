#!/usr/bin/python3
"""
Fabric script based on the file 1-pack_web_static.py that distributes an
archive to the web servers
"""

from fabric import Connection, task
from invoke.exceptions import UnexpectedExit
from os.path import exists

# Define the list of hosts
env_hosts = ['ubuntu@54.227.34.151', 'ubuntu@100.27.221.120']


@task
def do_deploy(c, archive_path):
    """Distributes an archive to the web servers"""
    if not exists(archive_path):
        return False
    
    try:
        file_name = archive_path.split("/")[-1]
        file_no_extension = file_name.split(".")[0]
        path = "/data/web_static/releases/"
        
        # Loop over each host to perform the deployment
        for host in env_hosts:
            conn = Connection(host)  # Create a connection for each host
            conn.put(archive_path, '/tmp/')  # Upload the archive
            conn.run(f'mkdir -p {path}{file_no_extension}/')  # Create directory
            conn.run(f'tar -xzf /tmp/{file_name} -C {path}{file_no_extension}/')  # Extract the archive
            conn.run(f'rm /tmp/{file_name}')  # Remove the archive from /tmp
            conn.run(f'mv {path}{file_no_extension}/web_static/* {path}{file_no_extension}/')  # Move files
            conn.run(f'rm -rf {path}{file_no_extension}/web_static')  # Clean up
            conn.run('rm -rf /data/web_static/current')  # Remove old symlink
            conn.run(f'ln -s {path}{file_no_extension}/ /data/web_static/current')  # Create new symlink
            
        return True
    except UnexpectedExit as e:
        print(f"Error: {e}")
        return False
