#!/usr/bin/python3
"""
Fabric script that generates a tgz archive from the contents of the web_static
folder of the AirBnB Clone repo
"""

from datetime import datetime
from fabric import task
from fabric.connection import Connection
from os.path import isdir


@task
def do_pack(c):
    """Generates a tgz archive"""
    try:
        date = datetime.now().strftime("%Y%m%d%H%M%S")
        if not isdir("versions"):
            c.run("mkdir versions")
        file_name = "versions/web_static_{}.tgz".format(date)
        c.run("tar -cvzf {} web_static".format(file_name))
        return file_name
    except Exception as e:
        print(f"Error: {e}")
        return None
