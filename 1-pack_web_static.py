#!/usr/bin/python3
"""
Fabric script that generates a tgz archive from the contents of the web_static
folder of the AirBnB Clone repo.
"""

from datetime import datetime
from fabric import Connection
from os.path import isdir


def do_pack():
    """
    Generates a tgz archive of the web_static folder.

    The archive is named using the current date and time in the format 
    YYYYMMDDHHMMSS and stored in the 'versions' directory. If the 'versions' 
    directory does not exist, it will be created.

    Returns:
        str: The path to the created tgz archive if successful, 
             or None if an error occurs.
    """
    try:
        # Get the current date and time to create a unique archive name
        date = datetime.now().strftime("%Y%m%d%H%M%S")
        
        # Check if the 'versions' directory exists; create it if it doesn't
        if not isdir("versions"):
            local("mkdir versions")

        # Define the filename for the archive
        file_name = "versions/web_static_{}.tgz".format(date)

        # Create a tgz archive of the web_static folder
        connection = Connection('localhost')  # Create a local connection
        connection.local("tar -cvzf {} web_static".format(file_name))

        # Return the path of the created archive
        return file_name
    except Exception as e:
        # Print the error message for debugging purposes
        print(f"Error: {e}")
        return None
