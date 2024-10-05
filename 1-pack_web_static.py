#!/usr/bin/python3
"""
Fabric script that generates a .tgz archive from the contents of the web_static.
"""

from datetime import datetime
from fabric.api import local
import os

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