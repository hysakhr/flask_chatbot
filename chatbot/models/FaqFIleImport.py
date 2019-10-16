from chatbot.database import db

from chatbot.models.Bot import BotModel

# This model does not save db


class FaqFileImportModel():
    def __init__(
            self,
            name: str,
            file_path: str,
            delimiter: str = '\t',
            bot: BotModel = None):
        self.name = name
        self.bot = bot
        self.file_path = file_path
        self.delimiter = delimiter
