import abc


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
