#!/usr/bin/python3
from fabric.api import local
from datetime import datetime


def do_pack():
    """Generates a .tgz archive from the contents of the web_static folder"""
    now = datetime.now()
    timestamp = now.strftime("%Y%m%d%H%M%S")
    archive_name = "web_static_" + timestamp + ".tgz"
    archive_path = "versions/{}".format(archive_name)
    local("mkdir -p versions")
    print("Packing web_static to {}".format(archive_path))
    result = local("tar -cvzf {} web_static".format(archive_path))
    if result.succeeded:
        size = (
            local("du -b {} | awk '{{print $1}}'"
                  .format(archive_path), capture=True)
        )
        print(f"web_static packed: {archive_path} -> {size.strip()}Bytes")
        return archive_path
    else:
        return None
