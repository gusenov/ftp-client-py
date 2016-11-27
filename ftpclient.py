#!/usr/bin/env python
"""ftpclient.py: Provides a connection to a FTP server."""

from enum import IntEnum
import ftplib
import os
import os.path
import time
import operator

__author__ = "Abbas Gussenov"

__license__ = "GPL"

class FtpItemIterator:
    def __init__(self, ftp_server):
        self.items = ftp_server.items
        self.idx = 0

    def __next__(self):
        if self.idx < len(self.items):
            result_item = self.items[self.idx]
            self.idx += 1
            return result_item
        else:
            raise StopIteration


class FtpItemType(IntEnum):
    cdir = 1,
    pdir = 2,
    dir = 3,
    file = 4,
    unknown = 5


class FtpItem:
    def __init__(self, line, parent_path):
        data, _, self.name = line.partition('; ')
        fields = data.split(';')
        for field in fields:
            field_name, _, field_value = field.partition('=')
            if field_name == 'type':
                if field_value == 'dir':
                    self.type = FtpItemType.dir
                elif field_value == 'cdir':
                    self.type = FtpItemType.cdir
                elif field_value == 'pdir':
                    self.type = FtpItemType.pdir
                elif field_value == 'file':
                    self.type = FtpItemType.file
                else:
                    self.type = FtpItemType.unknown

            elif field_name in ('sizd', 'size'):
                self.size = int(field_value)
            elif field_name == 'modify':
                self.mtime = field_value
            elif field_name == 'perm':
                self.perm = field_value
            elif field_name == 'unique':
                self.unique = field_value
            elif field_name == 'UNIX.group':
                self.nix_group = field_value
            elif field_name == 'UNIX.mode':
                self.nix_mode = field_value
            elif field_name == 'UNIX.owner':
                self.nix_owner = field_value

        self.full_path = os.path.join(parent_path, self.name)

        def mtime_as_secs(self):
            return time.mktime(time.strptime(self.mtime, '%Y%m%d%H%M%S'))


class FtpConnection:
    def __init__(self, host, port, user, password, logger):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.logger = logger

    def __enter__(self):
        self.site = ftplib.FTP()

        self.logger.info('Connecting to %s:%s...', self.host, self.port)
        self.site.connect(self.host, self.port)
        self.logger.info('Connection established')

        self.site.login(self.user, self.password)
        self.logger.info('Logged in')

        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.site.quit()
        self.logger.info('Disconnected from server')

    def walk(self, remote_dir='.', recursively=False):
        try:
            self.logger.info('CWD %s', remote_dir)
            self.site.cwd(remote_dir)

            items = []
            current_dir = self.site.pwd()

            self.logger.info('Retrieving directory listing of "%s"...', current_dir)
            self.site.retrlines('MLSD', lambda line: items.append(FtpItem(line, current_dir)))

            items.sort(key=operator.attrgetter('type', 'name'))

            for item in items:
                if item.type in (FtpItemType.cdir, FtpItemType.pdir):
                    continue
                yield item
                if recursively and item.type == FtpItemType.dir \
                        and item.type not in (FtpItemType.cdir, FtpItemType.pdir):
                    yield from self.walk(item.full_path, recursively)
        except ftplib.error_perm as response:
            self.logger.warning(response)


class FtpUtils:
    @staticmethod
    def formurl(user, password, host, port, remote_dir):
        slash = '/'
        if remote_dir.startswith('/'):
            slash = ''
        return 'ftp://{0}:{1}@{2}:{3}{4}{5}'.format(user, password, host, port, slash, remote_dir)
