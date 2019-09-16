import logging
from typing import Union
# from datetime import datetime
from dataclasses import dataclass

from db import SQLiteTableHandler
from entity import ScheduleRow
from db import SQL_DATETIME_NOW


logger = logging.getLogger(__name__)

DB_NAME = 'nba.db'


@dataclass
class ScheduleConfig:
    TABLE_NAME: str = 'schedule'
    COL_UPDATED_TIME: str = 'UPDATED_TIME'
    COL_ID: str = 'ID'
    COL_SEASON: str = 'SEASON'
    COL_DATE: str = 'DATE'
    COL_TIME: str = 'TIME'
    COL_H_TEAM: str = 'H_TEAM'
    COL_V_TEAM: str = 'V_TEAM'


cfg = ScheduleConfig()


class ScheduleDBHandler:
    def __init__(self):
        self.table_handler = SQLiteTableHandler(db_name=DB_NAME, table_name=cfg.TABLE_NAME)
        self.schedule_cols = [cfg.COL_ID, cfg.COL_SEASON, cfg.COL_DATE, cfg.COL_TIME,
                              cfg.COL_H_TEAM, cfg.COL_V_TEAM]

        self.default_order_by = f'{cfg.COL_ID} ASC'

    @property
    def ordered_cols(self):
        return self.schedule_cols[:] + [cfg.COL_UPDATED_TIME]

    def create_table(self):
        cols = {cfg.COL_ID: 'TEXT PRIMARY KEY NOT NULL',
                cfg.COL_SEASON: 'TEXT COLLATE NOCASE',
                cfg.COL_DATE: 'TEXT COLLATE NOCASE',
                cfg.COL_TIME: 'TEXT COLLATE NOCASE',
                cfg.COL_H_TEAM: 'TEXT COLLATE NOCASE',
                cfg.COL_V_TEAM: 'TEXT COLLATE NOCASE',
                cfg.COL_UPDATED_TIME: 'TEXT COLLATE NOCASE'
                }
        self.table_handler.create_table(',\n'.join([f'{k} {cols[k]}' for k in self.ordered_cols]))

    def insert_rows(self, schedule: [ScheduleRow]):
        for game in schedule:
            game_dict = dict(game._asdict())

            # game_dict[cfg.COL_UPDATED_TIME] = datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
            game_dict[cfg.COL_UPDATED_TIME] = SQL_DATETIME_NOW
            self.table_handler.insert_data(*list(zip(*game_dict.items())))

    def query_all_data(self, order_by=None, *args, **kwargs):
        if not order_by:
            order_by = self.default_order_by
        results = self.table_handler.query_all_data(self.ordered_cols, order_by, *args, **kwargs)
        return self.parse_response_rows(results)
    #
    # def query_if_schedule_id_exists(self, article_id):
    #     condition = f"{COL_ID}='{article_id}'"
    #     return self.table_handler.query_if_exists(condition)
    #
    # def select_schedule_by_condition(self, condition, order_by=None):
    #     if not order_by:
    #         order_by = self.default_order_by
    #     results = self.table_handler.query_selected_data(condition, order_by=order_by)
    #     return self.parse_response_rows(results)
    #
    # def select_nearest_news(self, n_units=None, unit='day'):
    #     if n_units:
    #         condition = f"{COL_PUBLISHED_TIME} >=  DATETIME('now', '-{n_units} {unit}')"
    #     else:
    #         condition = '1'
    #     # SELECT * FROM news WHERE PUBLISHED_TIME >=  DATETIME('now', '-3 month')
    #     # if not order_by:
    #     #     order_by = self.default_order_by
    #     results = self.table_handler.query_selected_data(condition, order_by=self.default_order_by)
    #     return self.parse_response_rows(results)
    #
    # def select_nearest_schedule_by_category(self, category, n_units=None, unit='day'):
    #     condition = f"{COL_CATEGORY} = '{category}'"
    #     if n_units:
    #         condition += f" AND ({COL_PUBLISHED_TIME} >=  DATETIME('now', '-{n_units} {unit}'))"
    #     results = self.table_handler.query_selected_data(condition, order_by=self.default_order_by)
    #     return self.parse_response_rows(results)
    #
    # def select_nearest_schedule_by_keyword(self, keyword, n_units=None, unit='day'):
    #     condition = f"({COL_CONTENT} LIKE '%{keyword}%' " \
    #                 f"OR {COL_KEYWORDS} LIKE '%{keyword}%'" \
    #                 f"OR {COL_POST_TAGS} LIKE '%{keyword}%')"
    #     if n_units:
    #         condition += f" AND {COL_PUBLISHED_TIME} >=  DATETIME('now', '-{n_units} {unit}')"
    #     results = self.table_handler.query_selected_data(condition, order_by=self.default_order_by)
    #     return self.parse_response_rows(results)
    #
    # def update_by_schedule_id(self, update_col, update_data, article_id):
    #     update_condition = f"{COL_ID} = '{article_id}'"
    #     return self.table_handler.update_data_by_condition(update_col, update_data, update_condition)

    def disconnect(self):
        self.table_handler.disconnect()

    def drop_table(self):
        self.table_handler.drop_table()

    def parse_response_rows(self, rows):
        sorted_articles = []
        for row in rows:
            sorted_articles.append(_prettify_query_result(dict(zip(self.ordered_cols, row))))
        return sorted_articles


def create_schedule_table():
    schedule_db = ScheduleDBHandler()
    schedule_db.create_table()
    schedule_db.disconnect()


def demo_restart():
    schedule_db = ScheduleDBHandler()
    schedule_db.drop_table()
    schedule_db.create_table()
    schedule_db.disconnect()


def clear_schedule_db():
    schedule_db = ScheduleDBHandler()
    schedule_db.table_handler.delete_all_data()
    schedule_db.disconnect()


def insert_schedules_to_db(schedules, print_inserted=True, n_limit_shows=10):
    if len(schedules) > 0:
        schedule_db = ScheduleDBHandler()
        schedule_db.insert_rows(schedules)
        if print_inserted:
            n_limits = min(n_limit_shows, len(schedules))
            results = schedule_db.query_all_data(order_by=f'{cfg.COL_ID} ASC', limit=n_limits)
            print(results)
        schedule_db.disconnect()

        return schedule_db.table_handler.counter
    else:
        return "No articles"


# def check_article_crawled(article_id):
#     schedule_db = ScheduleDBHandler()
#     is_existed = schedule_db.query_if_schedule_id_exists(article_id)
#     schedule_db.disconnect()
#
#     logger.debug(schedule_db.table_handler.counter)
#     return is_existed
#
#
# def query_nearest_news(n_days=None):
#     schedule_db = ScheduleDBHandler()
#     result = schedule_db.select_nearest_news(n_days)
#     schedule_db.disconnect()
#
#     logger.info(schedule_db.table_handler.counter)
#     return result
#
#
# def query_nearest_schedule_by_subscribed_category(category, n_days):
#     schedule_db = ScheduleDBHandler()
#     result = schedule_db.select_nearest_schedule_by_category(category, n_days)
#     schedule_db.disconnect()
#
#     logger.info(schedule_db.table_handler.counter)
#     return result
#
#
# def query_nearest_schedule_by_keyword(keyword, n_days):
#     schedule_db = ScheduleDBHandler()
#     result = schedule_db.select_nearest_schedule_by_keyword(keyword, n_days)
#     schedule_db.disconnect()
#
#     logger.info(f'result of query_nearest_schedule_by_keyword: {schedule_db.table_handler.counter}')
#     return result
#
#
# def update_column_by_schedule_id(update_col, update_data, article_id):
#     schedule_db = ScheduleDBHandler()
#     is_existed = schedule_db.update_by_schedule_id(update_col, f'"{update_data}"', f'"{article_id}"')
#     schedule_db.disconnect()
#     logger.info(f'result of update_column_by_schedule_id: {schedule_db.table_handler.counter}')
#     return is_existed
#
#
# def select_schedule_ids_with_empty_keywords():
#     schedule_db = ScheduleDBHandler()
#     results = schedule_db.select_schedule_by_condition(f'{COL_KEYWORDS} = "[]"')
#     schedule_db.disconnect()
#     logger.info(f'select_schedule_ids_with_empty_keywords: {schedule_db.table_handler.counter}')
#     return {r[COL_ID]: r[COL_LINK] for r in results
#             if r[COL_LINK].replace('https://buzzorange.com/techorange/', '')[0] == '2'}
#


def _prettify_query_result(single_result: Union[tuple, dict], col_names=None):
    if isinstance(single_result, tuple):
        assert len(single_result) == len(col_names)
        single_result = dict(zip(col_names, single_result))

    return single_result

