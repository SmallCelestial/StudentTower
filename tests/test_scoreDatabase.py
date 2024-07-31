import os
import unittest
from database.database_handler import ScoreDatabase
from constant_var import PROJECT_ROOT


class TestScoreDatabase(unittest.TestCase):
    def setUp(self):
        self.test_name_db = "test_scores.db"
        self.db = ScoreDatabase(self.test_name_db)

    def tearDown(self):
        self.db.connection.close()
        try:
            os.remove(os.path.join(PROJECT_ROOT, "database", self.test_name_db))
        except FileNotFoundError:
            print("File doesn't exist")

    def test_initialisation(self):
        expected_absolute_database_path = os.path.join(PROJECT_ROOT, "database", self.test_name_db)

        self.db.cursor.execute("PRAGMA database_list")
        database_list = self.db.cursor.fetchall()
        actual_absolute_database_path = None
        for row in database_list:
            if row[1] == 'main':
                actual_absolute_database_path = row[2]

        self.assertEqual(expected_absolute_database_path, actual_absolute_database_path)



