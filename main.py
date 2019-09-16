import time

from crawlers.schedule_crawler import ScheduleCrawler, SeleniumRequester

from parsers.parser import SchedulePageParser
from db.schedule_db_helper import demo_restart, insert_schedules_to_db
# from utils.file import save_pickle


def crawl_schedule(month):
    crawler = ScheduleCrawler(month)
    # crawler.home_page = 'saved/schedule_month_1.html'
    resp = crawler.crawl()
    # print(resp)

    if resp:
        parser = SchedulePageParser()
        games = parser.parse_game_list(resp)
        # saved_path = 'saved/schedule_page_{}.pickle'.format(month)
        return games


if __name__ == '__main__':
    demo_restart()
    # selenium_browser = SeleniumRequester()

    for month in range(1, 13):
        print(f'month: {month}')
        game_schedule = crawl_schedule(month)
        if game_schedule:
            # print([ for game in games])
            insert_schedules_to_db(game_schedule)
            time.sleep(10)

    # selenium_browser.driver.quit()

