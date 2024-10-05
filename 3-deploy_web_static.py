#!/usr/bin/python3
"""a Fabric script that creates and distributes an archive to your web servers"""

from fabric.api import local, env, put, run
import os
import datetime
env.hosts = ['54.196.153.63', '54.227.59.25']

def do_pack():
    """"
    generates a tgz archive
    return:  the archive path if the archive has been correctly generated.
    """
    try:
        time = datetime.now().strftime("%Y%m%d%H%M%S")
        if not os.path.exists("versions"):
            os.makedirs("versions")
        path = f"versions/web_static_{time}.tgz"
        local(f"tar -cvzf {path} web_static")
        return path
    except:
        return None


def do_deploy(archive_path):
    """
    Distributes an archive to web servers
    returns: True if all operations have been done correctly, 
    otherwise returns False.
    """
    if not os.path.exists(archive_path):
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

def deploy():
    """calls do_pack and do_deploy"""
    archive_path = do_pack()
    if archive_path is None:
        return False
    return do_deploy(archive_path)