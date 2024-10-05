#!/usr/bin/python3
"""
Fabric script that generates a .tgz archive from the contents of the web_static.
"""

from datetime import datetime
from invoke import run
from fabric import task
import os

@task
def do_pack(c):
    """
    Generates a .tgz archive from the contents of the web_static folder.
    Returns the archive path if the archive has been correctly generated.
    """
    try:
        time = datetime.now().strftime("%Y%m%d%H%M%S")
        if not os.path.exists("versions"):
            os.makedirs("versions")
        path = f"versions/web_static_{time}.tgz"
        c.run(f"tar -cvzf {path} web_static")  # Using context for execution
        return path
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
