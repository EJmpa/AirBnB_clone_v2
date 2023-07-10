#!/usr/bin/python3
"""Creates and distributes an archive to web servers using Fabric"""

from fabric.api import *
from datetime import datetime
from os import path

env.hosts = ['100.25.133.51', '3.83.227.219']
env.user = 'ubuntu'
env.key_filename = '~/.ssh/school'


def do_pack():
    """Generates a .tgz archive from the contents of the web_static folder"""
    now = datetime.now()
    timestamp = now.strftime("%Y%m%d%H%M%S")
    archive_name = "web_static_" + timestamp + ".tgz"
    archive_path = "versions/{}".format(archive_name)
    local("mkdir -p versions")
    print("Packing web_static to {}".format(archive_path))
    result = local("tar -czvf {} web_static \
    ".format(archive_path))
    if result.succeeded:
        size = local("stat -c %s {} \
        ".format(archive_path), capture=True)
        print("web_static packed: {} -> {}Bytes".format(archive_path, size))
        return archive_path
    else:
        return None


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
        run("sudo mkdir -p /data/web_static/releases/{}/"
            .format(archive_folder))
        run("sudo tar -xzf /tmp/{} -C /data/web_static/releases/{}/"
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


def deploy():
    """Creates and distributes an archive to web servers"""
    archive_path = do_pack()
    if not archive_path:
        return False
    return do_deploy(archive_path)
