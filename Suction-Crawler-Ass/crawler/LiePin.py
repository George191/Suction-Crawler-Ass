from bs4 import BeautifulSoup
from tools.proxy import Proxy
import warnings
import random
import logging
import time
import os
import urllib3
import pandas as pd

warnings.filterwarnings("ignore")


class CompanyInfo:

    def __init__(self):
        super(CompanyInfo).__init__()

        logging.basicConfig(level=logging.WARNING,
                            format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        self.config = Proxy()
        self.url = self.config.proxies(key='LiePinUrl')
        self.response = urllib3.PoolManager().request('GET', self.url, headers=self.proxies())
        self.logger.info(f'The Current Status Code: {self.response.status}')
        assert self.response.status == 200
        self.soup = BeautifulSoup(self.response.data.decode('utf-8'))
        self.company = dict()
        self.result = list()
        self.TotalCount = 100

    def proxies(self):
        user_agent = self.config.proxies(key='User-Agent')
        admin = ['http', 'https']
        header = random.choice(user_agent.get('Header'))
        ip = random.choice(user_agent.get('IP'))
        user_agent = {'User-Agent': header, random.choice(admin): ip}
        self.logger.info(f'The Current Header Params: {user_agent}')
        return user_agent

    def analysis_city(self):
        city = self.soup.find(name='div', attrs={'class': 'place-name'}).find_all(name='a')
        city = {element.text: element.get('href') for element in city[:-1]}
        for place, url in city.items():
            self.logger.info(f'The city currently being acquired: {place}')
            self.analysis_company(place, url)
        self.save_company()

    def analysis_company(self, place: str, url: str):
        for self.PageCount in range(self.TotalCount):
            self.logger.info(f'Getting information: {place} {self.PageCount + 1} page/Surplus {self.TotalCount} pages')
            response = urllib3.PoolManager().request('GET', url + 'pn' + str(self.PageCount), headers=self.proxies())
            self.logger.info(f'The Current Status Code: {response.status}')
            assert self.response.status == 200
            soup = BeautifulSoup(response.data.decode('utf-8'))
            company_item = soup.find_all(name='div', attrs={'class': 'list-item'})
            for company in company_item:
                self.company['city'] = place
                self.company['company_name'] = company.find('a').get('title')
                company_welfare = company.find(name='p', attrs={'class': 'boon-box'}).find_all('span')
                self.company['company_welfare'] = ','.join([welfare.text for welfare in company_welfare])
                self.company['company_industry'] = company.find(name='span', attrs={'class': 'industry'}).get('title')
                self.result.append(self.company)

            time.sleep(random.randint(0, 5))

    def save_company(self, path=None):
        if not path:
            path = os.path.join(os.path.abspath(os.path.dirname(os.getcwd())), self.config.proxies('LiePinData'))
        result = pd.DataFrame(self.result)
        result.to_csv(path, header=None, index=None, encoding='utf-8')
