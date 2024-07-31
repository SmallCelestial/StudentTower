import sqlite3
from constant_var import PROJECT_ROOT


class ScoreDatabase:
    def __init__(self, database_name: str):
        self.database_name = database_name
        absolute_path = PROJECT_ROOT + "/database/" + database_name
        self.connection = sqlite3.connect(absolute_path)
        self.cursor = self.connection.cursor()

        self.cursor.execute("CREATE TABLE IF NOT EXISTS scores ("
                            "id INTEGER PRIMARY KEY AUTOINCREMENT,"
                            "score INTEGER)")

        self.connection.commit()

    def add_score(self, score):
        self.cursor.execute("INSERT INTO scores (score)"
                            "VALUES (?)", (score, ))
        self.connection.commit()

    def get_max_score(self):
        self.cursor.execute("SELECT MAX(score) FROM scores")
        result = self.cursor.fetchone()[0]
        return result


