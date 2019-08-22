import requests
from bs4 import BeautifulSoup
from config.proxy import Proxy
import warnings
import random
import logging
import time
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
        self.response = requests.get(self.url, params=self.proxies())
        self.logger.info(f'The Current Status Code: {self.response.status_code}')
        self.soup = BeautifulSoup(self.response.text)
        self.result = dict()
        self.PageCount = 0
        self.TotalCount = 100

    def proxies(self):
        user_agent = self.config.proxies(key='User-Agent')
        admin = ['http', 'https']
        header = random.choice(user_agent.get('Header'))
        ip = random.choice(user_agent.get('IP'))
        user_agent = {'User-Agent': header, random.choice(admin): ip}
        self.logger.info(f'The Current Header Params: {user_agent}')
        return user_agent

    def analysis_html(self):
        city = self.soup.find(name='div', attrs={'class': 'place-name'}).find_all(name='a')

        city = {element.text: element.get('href') for element in city[:-2]}
        for place, url in city.items():
            self.logger.info(f'The city currently being acquired: {place}')
            self.analysis_company(place, url)

    def analysis_company(self, place, url):
        while self.TotalCount:
            self.logger.info(f'Getting information: {place} {self.PageCount} page  / Surplus {self.TotalCount} pages')
            response = requests.get(url + 'pn' + str(self.PageCount), params=self.proxies())
            self.logger.info(f'The Current Status Code: {self.response.status_code}')
            soup = BeautifulSoup(response.text)
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
