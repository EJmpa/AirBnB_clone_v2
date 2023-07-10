#!/usr/bin/python3
"""Distributes an archive to web servers using Fabric"""

from fabric.api import *
from os import path


env.hosts = ['100.25.133.51', '3.83.227.219']
env.user = 'ubuntu'
env.key_filename = '~/.ssh/school'


def do_deploy(archive_path):
    """Distributes an archive to web servers"""
    if not path.exists(archive_path):
        return False

    archive_filename = path.basename(archive_path)
    archive_folder = archive_filename.split('.')[0]

    try:
        # Upload the archive to /tmp/ directory
        put(archive_path, "/tmp/{}".format(archive_filename))

        # Uncompress the archive to /data/web_static/releases/
        run("sudo mkdir -p /data/web_static/releases/{}/".format(archive_folder))
        run("tar -xzf /tmp/{} -C /data/web_static/releases/{}/"
            .format(archive_filename, archive_folder))

        # Delete the archive from the web server
        run("sudo rm /tmp/{}".format(archive_filename))

        # Delete the symbolic link /data/web_static/current
        run("sudo rm -rf /data/web_static/current")

        # Create a new symbolic link to the new version
        run("sudo ln -s /data/web_static/releases/{}/ /data/web_static/current"
            .format(archive_folder))

        print("New version deployed!")
        return True
    except Exception as e:
        return False
