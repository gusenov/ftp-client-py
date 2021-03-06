from xml.etree import ElementTree
import os.path
import base64

from ftpclient.filezilla import *
# from ftpclient.filezilla.server import Server
# from ftpclient.filezilla.server_iterator import ServerIterator

__all__ = ["SiteManager"]


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
