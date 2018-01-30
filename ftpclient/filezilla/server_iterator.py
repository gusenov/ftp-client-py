__all__ = ["ServerIterator"]


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
