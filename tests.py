import unittest
from app import app
import os
import csv


class CsvReader(unittest.TestCase):
    def setUp(self):
        self.path = app.config["UPLOAD_FOLDER"]
        self.files = [
            f'{self.path}{file}'
            for file in os.listdir(
                self.path
                ) if file.endswith('.csv')
                ]

    def test_if_csv_files_are_read(self, files):
        files = self.files
        try:
            with open(files[0], newline='', encoding='utf-8') as csv_file:
                data = list(csv.reader(csv_file, delimiter=';'))
        except UnicodeDecodeError:
            with open(files[0], newline='', encoding='latin-1') as csv_file:
                data = list(csv.reader(csv_file, delimiter=';'))
        self.assertIsInstance(data, list)


if __name__ == '__main__':
    unittest.main()