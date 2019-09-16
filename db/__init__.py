import sqlite3
import logging
import inspect


logger = logging.getLogger(__name__)

SQL_DATETIME_NOW = "DATETIME('now', 'localtime')"


class SQLiteTableHandler:
    def __init__(self, db_name, table_name):
        self.db_name = db_name
        self.conn, self.cur = self.connect_db()
        self.table_name = table_name
        self.counter = {}

    def connect_db(self):
        try:
            conn = sqlite3.connect(self.db_name)
            cur = conn.cursor()
            logger.info('Database connected')
            return conn, cur
        except ConnectionRefusedError as e:
            logger.error(e)
            exit(1)

    def create_table(self, col_criteria):
        sql = f'CREATE TABLE {self.table_name} ({col_criteria});'
        self.execute_sql_with_e(sql)

    def drop_table(self):
        sql = f'DROP TABLE {self.table_name}'
        self.execute_sql_with_e(sql)

    def insert_data(self, input_column, input_data):
        sql = f"INSERT INTO {self.table_name} {input_column} VALUES {str(input_data)}"
        self.execute_sql_with_e(sql)

    def update_data_by_condition(self, setting_column, setting_data, update_condition):
        setting_condition = f"{setting_column} = {setting_data}"
        sql = f"UPDATE {self.table_name} SET {setting_condition} WHERE {update_condition}"
        self.execute_sql_with_e(sql)

    def query_all_data(self, sorted_cols, order_by='IDX DESC', *args, **kwargs):
        result = []
        select_cols = ','.join(sorted_cols)
        sql = f"SELECT {select_cols} FROM {self.table_name} ORDER BY {order_by}"

        if 'limit' in kwargs:
            sql += f' LIMIT {kwargs["limit"]}'

        exec_result = self.execute_sql_with_e(sql)
        if exec_result:
            data = self.cur.fetchall()
            for row in data:
                result.append(row)
        return result

    def query_selected_data(self, condition, no_case=False, order_by=None):
        result = []
        sql = f"SELECT * FROM {self.table_name} WHERE {condition}"
        if no_case:
            sql += " NO CASE"
        if order_by:
            sql += f" ORDER BY {order_by}"
        exec_result = self.execute_sql_with_e(sql)
        if exec_result:
            data = self.cur.fetchall()
            for row in data:
                result.append(row)
        return result

    def query_if_exists(self, condition):
        sql = f"SELECT EXISTS(SELECT * FROM {self.table_name} WHERE {condition})"
        self.execute_sql_with_e(sql)
        count = self.cur.fetchone()[0]
        if count > 0:
            return True
        return False

    def delete_all_data(self):
        sql = f"DELETE FROM {self.table_name} WHERE 1"
        self.execute_sql_with_e(sql)

    def disconnect(self):
        self.cur.close()  # 關閉游標
        self.conn.commit()  # 向資料庫中提交任何未解決的事務，對不支持事務的資料庫不進行任何操作
        self.conn.close()  # 關閉到資料庫的連接，釋放資料庫資源

    def execute_sql_with_e(self, sql):
        fn_name = str(inspect.stack()[1].function)
        counter = self.counter.setdefault(fn_name, {'success': 0, 'fail': 0})
        try:
            result = self.cur.execute(sql)
            logger.debug(f'{fn_name}() success.')
            counter['success'] += 1

            return result
        except Exception as e:
            counter['fail'] += 1
            print(sql)
            logger.info(f'Something wrong with {fn_name}, sql -> {sql}')
            logger.exception(e)
            return None


def _print_results(results, not_show_cols=None, n_prints=5):
    if not_show_cols is None:
        not_show_cols = []
    print('--- RESULTS ' + '-' * 80)
    for result in results[:n_prints]:
        for k, v in result.items():
            if k in not_show_cols:
                continue
            print(f'{k}: {v}')
        print('-' * 100)
    print(f'> Queried total {len(results)}.')


def _reformat_req_str(s):
    return s.replace('\\xa0', '').rstrip()


def _reformat_list_to_str(info: list):
    if len(info) > 0:
        if isinstance(info[0], int):
            info = [_reformat_req_str(str(i)) for i in info]
    return '\t'.join(info)

