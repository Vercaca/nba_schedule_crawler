import time

from crawlers.schedule_crawler import ScheduleCrawler

from parsers.parser import SchedulePageParser
from db.schedule_db_helper import demo_restart, insert_schedules_to_db


def crawl_schedule_by_month_idx(month_idx):
    crawler = ScheduleCrawler(month_idx)
    # crawler.home_page = 'saved/schedule_month_1.html'
    resp = crawler.crawl()

    if resp:
        parser = SchedulePageParser()
        games = parser.parse_game_list(resp)
        return games


def crawl_all_schedules():
    for month_idx in range(1, 13):
        if month_idx in [10, 11]:
            continue
        print(f'month: {month_idx}')
        game_schedule = crawl_schedule_by_month_idx(month_idx)
        if game_schedule:
            insert_schedules_to_db(game_schedule)
            time.sleep(10)


if __name__ == '__main__':
    demo_restart()
    crawl_all_schedules()
