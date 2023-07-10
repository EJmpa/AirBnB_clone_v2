#!/usr/bin/python3
"""Creates and distributes an archive to web servers using Fabric"""

from fabric.api import *
from fabric.contrib.files import exists
from datetime import datetime
import os

env.hosts = ['100.25.133.51', '3.83.227.219']
env.user = 'ubuntu'
env.key_filename = '~/.ssh/school'


def do_pack():
    """Create a tar gzipped archive of the directory web_static."""
    dt = datetime.utcnow()
    file = "versions/web_static_{}{}{}{}{}{}.tgz".format(dt.year,
                                                         dt.month,
                                                         dt.day,
                                                         dt.hour,
                                                         dt.minute,
                                                         dt.second)
    if not os.path.exists("versions"):
        os.makedirs("versions")
    if local("tar -cvzf {} web_static".format(file)).failed:
        return None
    return file


def do_deploy(archive_path):
    """Distributes an archive to a web server."""
    if not os.path.exists(archive_path):
        return False

    archive_filename = os.path.basename(archive_path)
    archive_folder = archive_filename.split('.')[0]

    try:
        # Upload the archive to /tmp/ directory
        put(archive_path, "/tmp/{}".format(archive_filename))

        # Create the target directory
        run("sudo mkdir -p /data/web_static/releases/{}/"
            .format(archive_folder))

        # Extract the archive
        run("sudo tar -xzf /tmp/{} -C /data/web_static/releases/{}/"
            .format(archive_filename, archive_folder))

        # Remove the archive
        run("sudo rm /tmp/{}".format(archive_filename))

        # Move files to the proper location
        run("sudo mv /data/web_static/releases/{}/web_static/* "
            "/data/web_static/releases/{}/"
            .format(archive_folder, archive_folder))

        # Remove the empty web_static directory
        run("sudo rm -rf /data/web_static/releases/{}/web_static"
            .format(archive_folder))

        # Remove the existing symbolic link
        run("sudo rm -rf /data/web_static/current")

        # Create a new symbolic link
        run("sudo ln -s /data/web_static/releases/{}/ /data/web_static/current"
            .format(archive_folder))

        print("New version deployed!")
        return True
    except Exception as e:
        return False


def deploy():
    """Create and distribute an archive to web servers."""
    archive_path = do_pack()
    if archive_path is None:
        return False
    return do_deploy(archive_path)
