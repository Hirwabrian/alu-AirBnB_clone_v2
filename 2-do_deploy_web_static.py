#!/usr/bin/python3
"""
Fabric script based on the file 1-pack_web_static.py that distributes an
archive to the web servers
"""

from fabric.api import put, run, env
from os.path import exists
env.hosts = ['54.196.153.63', '54.227.59.25']


def do_deploy(archive_path):
    """distributes an archive to the web servers"""
    if exists(archive_path) is False:
        return False
    try:
        file_name = archive_path.split('/')[-1]
        file_no_extension = file_name.split('.')[0]
        put(archive_path, f'/tmp/{file_name}')
        run(f'mkdir -p /data/web_static/releases/{file_no_extension}/')
        run(f"tar -xzf /tmp/{file_name} -C /data/web_static/releases/{file_no_extension}/")
        run(f'rm /tmp/{file_name}')
        run(f'mv /data/web_static/releases/{file_no_extension}/web_static/* /data/web_static/releases/{file_no_extension}/')
        run(f'rm -rf /data/web_static/releases/{file_no_extension}/web_static')
        run(f'rm -rf /data/web_static/current')
        run(f'ln -s /data/web_static/releases/{file_no_extension}/ /data/web_static/current')
        return True
    except:
        return False
