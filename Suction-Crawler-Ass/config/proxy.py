import yaml
import os
import warnings
warnings.filterwarnings("ignore")


class Proxy:

    def __init__(self, config=None):
        super(Proxy).__init__()
        self.config = config

    def proxies(self, server='Spider.config', key: str = None):
        if not self.config:
            self.config = yaml.load(open((os.path.join(os.getcwd(), 'config', 'config.yaml'))))
        spider = self.config.get(server)
        if not spider:
            raise NotImplementedError

        user_agent = spider.get(key)
        return user_agent

