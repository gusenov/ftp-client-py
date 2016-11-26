import os.path
from xml.etree import ElementTree
import base64


class ServerIterator:
    def __init__(self, site_manager):
        self.servers = site_manager.servers
        self.idx = 0

    def __next__(self):
        if self.idx < len(self.servers):
            result = self.servers[self.idx]
            self.idx += 1
            return result
        else:
            raise StopIteration


class Server:
    def __init__(self, host, port, user, password, name):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.name = name


class SiteManager:
    def __init__(self, path='~/.config/filezilla/sitemanager.xml'):
        self.tree = ElementTree.parse(os.path.expanduser(path))
        self.root = self.tree.getroot()
        self.servers = []

        for server in self.root.iter('Server'):
            host = server.find('Host').text
            port = int(server.find('Port').text)
            user = server.find('User').text

            pass_el = server.find('Pass')
            if pass_el.get('encoding') == 'base64':
                password = base64.b64decode(pass_el.text).decode('us-ascii')
            else:
                raise ValueError('unknown encoding')

            name = server.find('Name').text

            self.servers.append(Server(host, port, user, password, name))

    def __iter__(self):
        return ServerIterator(self)
