from filezilla import SiteManager
from ftpclient import FtpConnection
from ftpclient import FtpUtils
from storage import JsonStorage


def main():
    for server in SiteManager():
        user = server.user
        password = server.password
        host = server.host
        port = server.port

        db = JsonStorage("results", server.name)
        data = db.load()

        with FtpConnection(host, port, user, password) as conn:
            for item in conn.walk('.', True):
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
