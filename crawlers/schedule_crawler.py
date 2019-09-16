import abc
import logging

import requests
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup


logger = logging.getLogger(__name__)


CLS_SCHEDULE_CONTENT = 'Schedule-Content'


class BaseBS4Crawler(abc.ABC):
    home_page = None

    def __init__(self, requester, parser_feature='html.parser'):
        self.soup = None
        self.requester = requester
        self._parser_feature = parser_feature

    def boot(self, *args, **kwargs):
        self._setting(*args, **kwargs)

    @abc.abstractmethod
    def crawl(self):
        return NotImplemented

    @abc.abstractmethod
    def _setting(self, *args, **kwargs):
        """ set home page, save_result..."""
        return NotImplemented


class ScheduleCrawler(BaseBS4Crawler):
    home_page = 'https://stats.nba.com/schedule/#!?Month={}&PD=N'

    def __init__(self, month, team=None):
        super().__init__(requester=SeleniumRequester(), parser_feature='html.parser')
        # super().__init__(requester=DemoRequester(), parser_feature='html.parser')

        self._setting(month, team)

    def crawl(self):
        self._request(self.home_page)
        return self.soup

    def _setting(self, month, team):
        self.home_page = self.home_page.format(month)
        if team:
            self.home_page += '&TEAM={}'.format(team)

    def _request(self, page):
        html = self.requester.request(page)
        self.soup = BeautifulSoup(html, self._parser_feature) if html else None


class BaseRequestHandler(abc.ABC):
    @abc.abstractmethod
    def request(self, page, *args, **kwargs):
        return NotImplemented


class DemoRequester(BaseRequestHandler):
    def request(self, page, *args, **kwargs):
        with open(page) as f:
            return f.read()


class PythonRequester(BaseRequestHandler):
    def request(self, page, encoding='utf-8', *args, **kwargs):
        resp = requests.get(page)
        resp.encoding = encoding  # encoded with format utf-8 for chinese

        # 確認是否下載成功
        if resp.status_code == requests.codes.ok:
            return resp.text
        else:
            logger.error(f'Cannot parse page "{page}"')
            raise ConnectionRefusedError


class SeleniumRequester(BaseRequestHandler):
    @staticmethod
    def request(page, *args, **kwargs):
        chromeOptions = webdriver.ChromeOptions()
        prefs = {'profile.managed_default_content_settings.images': 2}
        chromeOptions.add_experimental_option("prefs", prefs)
        driver = webdriver.Chrome(chrome_options=chromeOptions)

        driver.get(page)
        # time.sleep(10)
        delay = 10  # seconds
        try:
            my_element = WebDriverWait(driver, delay).\
                until(EC.presence_of_element_located((By.CLASS_NAME, CLS_SCHEDULE_CONTENT)))
            # print("Page is ready!")
            # print('my element: ')
            # print(my_element)
            # print('-'*100)
        except TimeoutException:
            print("Loading took too much time!")

        html = driver.page_source
        driver.quit()

        return html
