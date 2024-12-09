import sqlite3


class SQLite:
    def __init__(self):
        self.path = "db.sqlite"
    def __enter__(self):
        self.connection = sqlite3.connect(self.path)
        self.connection.row_factory = sqlite3.Row
        self.cursor = self.connection.cursor()
        return self
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.close()

