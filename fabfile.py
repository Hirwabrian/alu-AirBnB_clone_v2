#!/usr/bin/python3
"""
A Fabric script that creates and distributes an archive to your web servers
"""

from fabric import task
import os
from datetime import datetime

env = {
    'hosts': ['54.196.153.63', '54.227.59.25']
}

@task
def do_pack(c):
    """
    Generates a tgz archive from the contents of the web_static folder.
    Returns the archive path if the archive has been correctly generated.
    """
    try:
        time = datetime.now().strftime("%Y%m%d%H%M%S")
        if not os.path.exists("versions"):
            os.makedirs("versions")
        path = f"versions/web_static_{time}.tgz"
        c.run(f"tar -cvzf {path} web_static")
        return path
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


@task
def do_deploy(c, archive_path):
    """
    Distributes an archive to web servers.
    Returns True if all operations have been done correctly, otherwise returns False.
    """
    if not os.path.exists(archive_path):
        return False
    try:
        file_name = archive_path.split('/')[-1]
        file_no_extension = file_name.split('.')[0]
        c.put(archive_path, f'/tmp/{file_name}')
        c.run(f'mkdir -p /data/web_static/releases/{file_no_extension}/')
        c.run(f"tar -xzf /tmp/{file_name} -C /data/web_static/releases/{file_no_extension}/")
        c.run(f'rm /tmp/{file_name}')
        c.run(f'mv /data/web_static/releases/{file_no_extension}/web_static/* /data/web_static/releases/{file_no_extension}/')
        c.run(f'rm -rf /data/web_static/releases/{file_no_extension}/web_static')
        c.run(f'rm -rf /data/web_static/current')
        c.run(f'ln -s /data/web_static/releases/{file_no_extension}/ /data/web_static/current')
        return True
    except Exception as e:
        print(f"An error occurred: {e}")
        return False


@task
def deploy(c):
    """
    Calls do_pack and do_deploy to create and distribute the archive.
    """
    archive_path = do_pack(c)
    if archive_path is None:
        return False
    return do_deploy(c, archive_path)

