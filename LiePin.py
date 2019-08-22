import requests
from bs4 import BeautifulSoup
from suction.config.proxy import Proxy
import warnings
import random
import logging
import time
warnings.filterwarnings("ignore")
LiePin = "https://www.liepin.com/company"


class CompanyInfo(object):

    def __init__(self, url):
        super(CompanyInfo).__init__()

        logging.basicConfig(level=logging.WARNING,
                            format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)

        self.url = url
        self.response = requests.get(self.url, params=self.proxies())
        self.logger.info(f'The Current Status Code: {self.response.status_code}')
        self.soup = BeautifulSoup(self.response.text, 'lxml')
        self.result = dict()
        self.PageCount = 0
        self.TotalCount = 100

    @staticmethod
    def proxies():
        ip = Proxy().IP
        agent = Proxy().Agent
        admin = ['http', 'https']
        return {'User-Agent': agent, random.choice(admin): ip}

    def analysis_html(self):
        city = self.soup.find(name='div', attrs={'class': 'place-name'}).find_all(name='a')
        city = {element.text: element.get('href') for element in city[:-2]}
        for place, url in city.items():
            self.logger.info(f'The city currently being acquired: {place}')
            self.analysis_company(place, url)

    def analysis_company(self, place, url):
        while self.TotalCount:
            self.logger.info(f'Getting {place} {self.PageCount} page of information / total {self.TotalCount} pages')
            response = requests.get(url + 'pn' + str(self.PageCount), params=self.proxies())
            soup = BeautifulSoup(response.text, 'lxml')
            company_item = soup.find_all(name='div', attrs={'class': 'list-item'})
            for company in company_item:
                self.result['city'] = place
                self.result['company_name'] = company.find('a').get('title')
                company_welfare = company.find(name='p', attrs={'class': 'boon-box'}).find_all('span')
                self.result['company_welfare'] = [welfare.text for welfare in company_welfare]
                self.result['company_industry'] = company.find(name='span', attrs={'class': 'industry'}).get('title')
            self.PageCount += 1
            self.TotalCount -= 1
            time.sleep(random.randint(0, 5))


spider = CompanyInfo(LiePin)
spider.analysis_html()

