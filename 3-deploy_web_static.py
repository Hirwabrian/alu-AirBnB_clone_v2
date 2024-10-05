#!/usr/bin/python3
"""
Fabric script based on the file 2-do_deploy_web_static.py that creates and
distributes an archive to the web servers
"""

from fabric import task
from datetime import datetime
import os


hosts = ['54.196.153.63', '54.227.59.25']
created_path = None

@task
def do_pack(c):
    """
    Generates a .tgz archive from the contents of web_static
    """
    time = datetime.now().strftime('%Y%m%d%H%M%S')
    file_name = "versions/web_static_{}.tgz".format(time)
    try:
        
        c.local("mkdir -p ./versions")
        c.local("tar --create --verbose -z --file={} ./web_static"
                .format(file_name))
        return file_name
    except Exception:
        return None

@task
def do_deploy(c, archive_path):
    """
    Using fabric to distribute an archive
    """
    if not os.path.isfile(archive_path):
        return False
    try:
        archive = archive_path.split("/")[-1]
        path = "/data/web_static/releases"
        c.put(archive_path, "/tmp/{}".format(archive))
        folder = archive.split(".")[0]
        c.run("mkdir -p {}/{}/".format(path, folder))
        c.run("tar -xzf /tmp/{} -C {}/{}/"
              .format(archive, path, folder))
        c.run("rm /tmp/{}".format(archive))
        c.run("mv {}/{}/web_static/* {}/{}/"
              .format(path, folder, path, folder))
        c.run("rm -rf {}/{}/web_static".format(path, folder))
        c.run("rm -rf /data/web_static/current")
        c.run("ln -sf {}/{} /data/web_static/current"
              .format(path, folder))
        return True
    except Exception:
        return False

@task
def deploy(c):
    """
    Deploy function that creates and distributes an archive
    """
    global created_path
    created_path = do_pack(c)
    if created_path is None:
        return False
    return do_deploy(c, created_path)
