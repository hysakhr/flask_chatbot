from chatbot.database import db

# This model does not save db


class FaqFileImportModel():
    def __init__(self, name: str, file_path: str, delimiter: str = '\t'):
        self.name = name
        self.file_path = file_path
        self.delimiter = delimiter
