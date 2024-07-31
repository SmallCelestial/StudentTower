import os
import unittest
from database.database_handler import ScoreDatabase
from constants import PROJECT_ROOT


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

    def test_add_score(self):
        self.db.add_score(100)
        self.db.add_score(100)

        self.db.cursor.execute("SELECT score FROM scores")
        scores = tuple(score[0] for score in self.db.cursor.fetchall())

        self.assertEqual(scores, (100, 100))

    def test_get_max_score(self):
        self.db.add_score(100)
        self.db.add_score(150)
        self.db.add_score(200)
        expected_max_score = 200

        actual_max_score = self.db.get_max_score()

        self.assertEqual(expected_max_score, actual_max_score)
