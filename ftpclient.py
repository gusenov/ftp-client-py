from enum import Enum
import ftplib
import logging
import os
import os.path
import time


def ftpclientlogger(path_to_results_dir, log_file_name):
    if not os.path.exists(path_to_results_dir):
        os.makedirs(path_to_results_dir)

    path_to_log_file = os.path.join(path_to_results_dir, log_file_name)
    if os.path.exists(path_to_log_file):
        os.remove(path_to_log_file)

    fh = logging.FileHandler(path_to_log_file)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)

    logger = logging.getLogger('FtpClientLogger')
    logger.setLevel(logging.DEBUG)
    logger.addHandler(fh)

    return logger

ftp_client_log = ftpclientlogger('results', 'ftp_client.log')


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


class FtpItemType(Enum):
    dir = 1,
    cdir = 2,
    pdir = 3,
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
    def __init__(self, host, port, user, password):
        self.host = host
        self.port = port
        self.user = user
        self.password = password

    def __enter__(self):
        self.site = ftplib.FTP()
        self.site.connect(self.host, self.port)
        self.site.login(self.user, self.password)

        ftp_client_log.info('🛈 Successfully connected to %s:%s', self.host, self.port)

        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.site.quit()

        ftp_client_log.info('🛈 Disconnected from %s:%s', self.host, self.port)

    def walk(self, remote_dir='.', recursively=False):
        try:
            self.site.cwd(remote_dir)

            ftp_client_log.info('🛈 Changed directory to "%s"', remote_dir)

            items = []
            parent_dir = self.site.pwd()

            ftp_client_log.info('🛈 Retrieving directory listing of "%s"...', parent_dir)

            self.site.retrlines('MLSD', lambda line: items.append(FtpItem(line, parent_dir)))
            for item in items:
                if item.type in (FtpItemType.cdir, FtpItemType.pdir):
                    continue
                if recursively and item.type == FtpItemType.dir \
                        and item.type not in (FtpItemType.cdir, FtpItemType.pdir):
                    yield from self.walk(item.full_path, recursively)
                yield item
        except ftplib.error_perm as response:

            if __debug__:
                url = FtpUtils.formurl(self.user, self.password, self.host, self.port, remote_dir)
                ftp_client_log.warning('𝍌 %s', url)


class FtpUtils:
    @staticmethod
    def formurl(user, password, host, port, remote_dir):
        slash = '/'
        if remote_dir.startswith('/'):
            slash = ''
        return 'ftp://{0}:{1}@{2}:{3}{4}{5}'.format(user, password, host, port, slash, remote_dir)
