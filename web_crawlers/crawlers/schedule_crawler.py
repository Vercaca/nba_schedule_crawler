import logging

from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

from web_crawlers.crawlers import BaseBS4Crawler
from web_crawlers.requesters import SeleniumRequester
from web_crawlers.parsers.schedule_page_parser import CLS_SCHEDULE_CONTENT


logger = logging.getLogger(__name__)


class ScheduleCrawler(BaseBS4Crawler):
    home_page = 'https://stats.nba.com/schedule/#!?Month={month_idx}&PD=N'

    def __init__(self, month_idx, team=None):
        super().__init__(requester=SeleniumRequester(), parser_feature='html.parser')
        # super().__init__(requester=DemoRequester(), parser_feature='html.parser')

        self._setting(month_idx, team)

    def crawl(self):
        self._request(self.home_page)
        return self.soup

    def _setting(self, month_idx, team):
        self.home_page = self.home_page.format(month_idx=month_idx)
        if team:
            self.home_page += '&TEAM={}'.format(team)

    def _request(self, page):
        html = self.requester.request(page=page, condition=(By.CLASS_NAME, CLS_SCHEDULE_CONTENT))
        self.soup = BeautifulSoup(html, self._parser_feature) if html else None
