import sqlite3
from datetime import datetime, timedelta


class DateTime:
    def __init__(self):
        self.timer = int
        self.rounded_time = int
        self.clock_in_time = None
        self.clock_out_time = None
        self.datetime_str = str

    def datetime_to_str(self, dt: datetime):
        self.datetime_str = dt.strftime("%Y-%m-%d %H:%M")
        return self.datetime_str

    def clock_in(self) -> datetime:
        current_datetime = datetime.now().replace(second=0, microsecond=0)
        self.clock_in_time = current_datetime
        return self.clock_in_time

    def clock_out(self) -> datetime:
        current_datetime = datetime.now().replace(second=0, microsecond=0)
        self.clock_out_time = current_datetime
        return self.clock_out_time

    def calculate(self, io_data: tuple):
        pass

    # initially it was rounding time. then i saw it would be redundant
    def round_and_save(self, io: str, round_value: int) -> datetime:
        if io == "in":
            initial_time = datetime.now().replace(second=0, microsecond=0)
            # for rounding UP we need to add round_value to minutes
            # then // the minutes to get some number and multiply it by round_value
            rounded_time = initial_time + timedelta(minutes=round_value)
            rounded_time = rounded_time.replace(minute=(rounded_time.minute // round_value) * round_value)
            self.clock_in_time = rounded_time
            self.datetime_to_str(rounded_time)
            return self.clock_in_time

        elif io == "out":
            initial_time = datetime.now().replace(second=0, microsecond=0)
            rounded_minute = initial_time.minute % round_value
            rounded_time = initial_time - timedelta(minutes=rounded_minute)
            self.clock_out_time = rounded_time
            self.datetime_to_str(rounded_time)
            return self.clock_out_time


class Database:
    def __init__(self, database_file="work_hrs.db"):
        self.database_file = database_file

    def connect(self):
        connection = sqlite3.connect(self.database_file)
        return connection

    def check_table_existence(self, user_id):
        connection = sqlite3.connect(self.database_file)
        cursor = connection.cursor()
        sql_statement = "SELECT name FROM sqlite_master WHERE type='table' AND name=?;"
        cursor.execute(sql_statement, (user_id,))
        result = cursor.fetchall()
        connection.close()
        return result

    def check_settings_existence(self, user_id):
        connection = sqlite3.connect(self.database_file)
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM settings WHERE user_id = ?;", (user_id,))
        result = cursor.fetchone()
        connection.close()
        return result

    def create(self, user_id: int):
        connection = sqlite3.connect(self.database_file)
        cursor = connection.cursor()
        cursor.execute(f"CREATE TABLE IF NOT EXISTS '{user_id}' ("
                       f"id INTEGER PRIMARY KEY AUTOINCREMENT,"
                       f"clock_in TEXT, "
                       f"clock_out TEXT, "
                       f"hour_minute_total TEXT, "
                       f"hour_total REAL, "
                       f"minute_total INTEGER);")
        connection.commit()
        connection.close()

    def insert(self, user_id: int, col_name: str, value: datetime):
        connection = sqlite3.connect(self.database_file)
        cursor = connection.cursor()
        value = value.strftime("%Y-%m-%d %H:%M")
        sql_statement = f"INSERT INTO '{user_id}' ({col_name}) VALUES (?);"
        cursor.execute(sql_statement, (value,))
        connection.commit()
        connection.close()

    def delete(self, user_id, row_id: int):
        connection = sqlite3.connect(self.database_file)
        cursor = connection.cursor()
        sql_statement = f"DELETE FROM '{user_id}' WHERE id = ?;"
        cursor.execute(sql_statement, (row_id,))
        connection.commit()
        connection.close()

    def update(self, user_id, old_value, new_value, row_id: int):
        connection = sqlite3.connect(self.database_file)
        cursor = connection.cursor()
        sql_statement = f"UPDATE '{user_id}' SET ? = ? WHERE id = ?;"
        cursor.execute(sql_statement, (old_value, new_value, row_id))
        connection.commit()
        connection.close()

    def is_last_cell_filled(self, user_id) -> tuple:
        connection = sqlite3.connect(self.database_file)
        cursor = connection.cursor()
        sql_statement = f"SELECT * FROM '{user_id}' ORDER BY id DESC LIMIT 1"
        cursor.execute(sql_statement)
        query_result = cursor.fetchone()
        connection.close()
        return query_result


class Settings(Database):
    def __init__(self):
        super(Database).__init__()
        self.round_value = int

        connection = sqlite3.connect(self.database_file)
        cursor = connection.cursor()
        cursor.execute(f"CREATE TABLE IF NOT EXISTS settings' ("
                       f"id INTEGER PRIMARY KEY UNIQUE, "
                       f"username TEXT, "
                       f"firstname TEXT, "
                       f"lastname TEXT, "
                       f"is_premium BOOLEAN, "
                       f"language TEXT, "
                       f"workplace TEXT, "
                       f"position TEXT, "
                       f"salary INTEGER, "
                       f"round_to INTEGER);")
        connection.commit()
        connection.close()
