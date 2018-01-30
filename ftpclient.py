#!/usr/bin/env python
"""ftpclient.py: Provides a connection to a FTP server."""

from ftpclient import *
from ftpclient.filezilla import *

__license__ = "MIT License"
__author__ = "Abbas Gussenov"


def main():
    for server in SiteManager():
        user = server.user
        password = server.password
        host = server.host
        port = server.port

        filelogger = FtpClientFileLogger('results', 'ftp_client.log').logger
        with FtpConnection(host, port, user, password, filelogger) as conn:
            for item in conn.walk(remote_dir='.', recursively=True):
                path = item.full_path
                url = FtpUtils.formurl(user, password, host, port, path)
                print("{0} {1}".format(item.mtime, url))


if __name__ == "__main__":
    main()
