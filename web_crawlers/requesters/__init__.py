import abc
import logging

import requests
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


logger = logging.getLogger(__name__)


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
    def request(page, condition=None, *args, **kwargs):
        chrome_options = webdriver.ChromeOptions()
        prefs = {'profile.managed_default_content_settings.images': 2}
        chrome_options.add_experimental_option("prefs", prefs)
        driver = webdriver.Chrome(chrome_options=chrome_options)

        driver.get(page)
        delay = 10  # seconds
        if condition:
            try:
                WebDriverWait(driver, delay).\
                    until(EC.presence_of_element_located(condition))
            except TimeoutException:
                print("Loading took too much time!")

        html = driver.page_source
        driver.quit()

        return html
