""" Define database """
from tinydb import TinyDB


class Database:
    """Database class"""

    def __init__(self):
        """Init attributes:
        file_path - file path to create the json file
        db - tinydb instance

        Init method:
        load_db - load tinydb instance from json file"""

        self.file_path = "db.json"
        self.db = None

        self.load_db()

    def create_empty_db(self):
        """Creates an empty database JSON file if needed."""

        with open(self.file_path, "w"):
            pass

    def load_db(self):
        """Loads a TinyDB object from a JSON file."""

        try:
            self.db = TinyDB(self.file_path)
        except FileNotFoundError:
            self.create_empty_db()
            self.load_db()
