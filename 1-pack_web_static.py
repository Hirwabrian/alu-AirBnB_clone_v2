#!/usr/bin/python3
"""
Fabric script that generates a .tgz archive from the contents 
of the web_static folder of the AirBnB Clone repository.
"""

from datetime import datetime
from fabric import task
from os.path import isdir

@task
def do_pack(c):
    """
    Generates a .tgz archive from the contents of the web_static folder.

    Args:
        c (Connection): A Fabric Connection object that provides 
                        methods for running commands on a remote server.

    Returns:
        str: The path to the generated .tgz file if successful; 
              None if there was an error during the process.
    """
    try:
        # Generate a timestamp to create a unique filename
        date = datetime.now().strftime("%Y%m%d%H%M%S")

        # Check if the "versions" directory exists; if not, create it
        if not isdir("versions"):
            c.run("mkdir versions")
        
        # Define the name of the archive file
        file_name = "versions/web_static_{}.tgz".format(date)

        # Create a .tgz archive of the web_static folder
        c.run("tar -cvzf {} web_static".format(file_name))

        # Return the path to the created archive
        return file_name
    except Exception as e:
        # Print the error message and return None if an exception occurs
        print(f"Error: {e}")
        return None
