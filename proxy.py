from suction.config import config
import random


class Proxy(object):

    def __init__(self):
        super(Proxy).__init__()

        self.IP = random.choice(config.IP)
        self.Agent = random.choice(config.user_Agent)

