from crawler.LiePin import CompanyInfo
import pandas as pd
from tools.proxy import Proxy
import os


class QiChaCha(CompanyInfo):

    def __init__(self):
        super(QiChaCha, self).__init__()
        self.analysis_city()
        self.name = None
        self.config = Proxy()

    def company(self, path=None):
        if not path:
            path = self.config.proxies(key='LiePinData')
        self.name = pd.read_csv(os.path.join(os.getcwd(), path))['company_name'].tolist()

    # def analysis_QiChaCha(self):


if __name__ == '__main__':
    demo = QiChaCha()




