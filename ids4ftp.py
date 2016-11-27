import logging
import os.path
from filezilla import SiteManager
from ftpclient import FtpConnection
from ftpclient import FtpUtils
from storage import JsonStorage


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


def main():
    for server in SiteManager():
        user = server.user
        password = server.password
        host = server.host
        port = server.port

        db = JsonStorage("results", server.name)
        data = db.load()

        with FtpConnection(host, port, user, password, ftpclientlogger('results', 'ftp_client.log')) as conn:
            for item in conn.walk(remote_dir='.', recursively=True):
                path = item.full_path
                if path in data:
                    if data[path] != item.mtime:
                        url = FtpUtils.formurl(user, password, host, port, path)
                        print("☢ {0}", url)
                else:
                    data[path] = item.mtime

        db.save(data)

if __name__ == "__main__":
    main()
