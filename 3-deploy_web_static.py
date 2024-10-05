#!/usr/bin/python3
"""
A Fabric script that creates and distributes an archive to web servers.

This script provides three main tasks:
1. `do_pack`: Creates a `.tgz` archive from the `web_static` directory.
2. `do_deploy`: Uploads and extracts the archive on web servers.
3. `deploy`: Combines both packing and deployment into one task.

The script is intended to be executed with Fabric 3.
"""

from fabric import task
import os
from datetime import datetime

# Set the web server IP addresses
env = {
    'hosts': ['54.196.153.63', '54.227.59.25']
}

@task
def do_pack(c):
    """
    Generates a `.tgz` archive from the contents of the `web_static` folder.

    This task compresses the contents of the `web_static` directory into a 
    `.tgz` archive and stores it in a `versions` directory, which is created 
    if it does not already exist.

    Args:
        c (Connection): Fabric's connection object used to run commands locally.

    Returns:
        str: The path to the generated archive file if successful.
        None: If any exception occurs during the creation process.

    Raises:
        Exception: If the archive creation fails.
    """
    try:
        # Get the current timestamp to name the archive file uniquely
        time = datetime.now().strftime("%Y%m%d%H%M%S")
        # Create the 'versions' directory if it does not exist
        if not os.path.exists("versions"):
            os.makedirs("versions")
        # Define the path for the archive
        path = f"versions/web_static_{time}.tgz"
        # Create the archive
        c.run(f"tar -cvzf {path} web_static")
        return path
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


@task
def do_deploy(c, archive_path):
    """
    Distributes an archive to web servers and configures the web content.

    This task uploads the specified archive to the `/tmp/` directory on the
    remote server, unpacks it into the `/data/web_static/releases/` directory,
    and updates the symbolic link for the current version.

    Args:
        c (Connection): Fabric's connection object used to run commands on remote servers.
        archive_path (str): The path to the archive file to be deployed.

    Returns:
        bool: True if the deployment was successful, False otherwise.

    Raises:
        Exception: If any operation fails, such as file transfer or extraction.
    """
    if not os.path.exists(archive_path):
        return False
    try:
        # Extract the archive file name and its base name without extension
        file_name = archive_path.split('/')[-1]
        file_no_extension = file_name.split('.')[0]
        
        # Upload the archive to the /tmp/ directory on the server
        c.put(archive_path, f'/tmp/{file_name}')
        
        # Create a directory for the new release
        c.run(f'mkdir -p /data/web_static/releases/{file_no_extension}/')
        
        # Extract the archive contents
        c.run(f"tar -xzf /tmp/{file_name} -C /data/web_static/releases/{file_no_extension}/")
        
        # Remove the archive from the temporary directory
        c.run(f'rm /tmp/{file_name}')
        
        # Move the content out of the web_static folder
        c.run(f'mv /data/web_static/releases/{file_no_extension}/web_static/* /data/web_static/releases/{file_no_extension}/')
        
        # Remove the now empty web_static directory
        c.run(f'rm -rf /data/web_static/releases/{file_no_extension}/web_static')
        
        # Remove the current symbolic link to the old release
        c.run(f'rm -rf /data/web_static/current')
        
        # Create a new symbolic link pointing to the new release
        c.run(f'ln -s /data/web_static/releases/{file_no_extension}/ /data/web_static/current')
        
        return True
    except Exception as e:
        print(f"An error occurred: {e}")
        return False


@task
def deploy(c):
    """
    Combines `do_pack` and `do_deploy` to create and distribute an archive.

    This task first creates an archive by calling `do_pack`, then deploys it
    to the web servers using `do_deploy`. This is a high-level task meant to
    streamline the full deployment process.

    Args:
        c (Connection): Fabric's connection object used to run commands on local and remote hosts.

    Returns:
        bool: True if both packing and deployment succeed, False otherwise.

    Raises:
        Exception: If either `do_pack` or `do_deploy` fails.
    """
    # Call do_pack to generate the archive
    archive_path = do_pack(c)
    
    # If do_pack failed, return False
    if archive_path is None:
        return False
    
    # Call do_deploy to distribute the archive to the servers
    return do_deploy(c, archive_path)
