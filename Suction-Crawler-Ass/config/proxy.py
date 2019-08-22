import yaml
import os


class Proxy(object):

    def __init__(self, config=None):
        super(Proxy).__init__()
        self.config = config

    def proxies(self, server='Spider.config', key: str = None):
        if not self.config:
            self.config = yaml.load(open(os.path.dirname(os.path.realpath(__file__)) + '/config.yaml'))

        spider = self.config.get(server)
        if not spider:
            raise NotImplementedError

        user_agent = spider.get(key)
        return user_agent


Proxy().proxies(key='User-Agent')