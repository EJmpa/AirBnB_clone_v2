#!/usr/bin/python3
from fabric.api import local
from datetime import datetime


def do_pack():
    """Generates a .tgz archive from the contents of the web_static folder"""
    now = datetime.now()
    timestamp = now.strftime("%Y%m%d%H%M%S")
    archive_name = "web_static_" + timestamp + ".tgz"
    archive_path = "versions/{}".format(archive_name)
    local("mkdir -p versions > /dev/null 2>&1")
    print("Packing web_static to {}".format(archive_path))
    result = local("tar -czvf {} web_static \
    > /dev/null 2>&1".format(archive_path))
    if result.succeeded:
        size = local("stat -c %s {} \
        > /dev/null 2>&1".format(archive_path), capture=True)
        print("web_static packed: {} -> {}Bytes".format(archive_path, size))
        return archive_path
    else:
        return None
