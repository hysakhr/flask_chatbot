import os
import csv

from chatbot.database import db
from chatbot.admin.domain.repositories.FaqRepository import IFaqRepository
from chatbot.admin.domain.repositories.FaqListRepository import IFaqListRepository
from chatbot.models.Faq import FaqModel
from chatbot.models.FaqList import FaqListModel
from chatbot.models.FaqFIleImport import FaqFileImportModel
from chatbot.models.Bot import BotModel


class FaqFileImportService:
    def __init__(self, faq_repository: IFaqRepository,
                 faq_list_repository: IFaqListRepository):
        self.faq_repository = faq_repository
        self.faq_list_repository = faq_list_repository

    def get_new_obj(self, bot: BotModel = None):
        return FaqFileImportModel(name='', file_path='', bot=bot)

    def import_tsv(self, faq_file_import: FaqFileImportModel):
        if not os.path.exists(faq_file_import.file_path):
            return False

        session = db.Session()
        try:
            # db operation
            faq_list = FaqListModel(
                name=faq_file_import.name,
                bot_id=faq_file_import.bot.id)
            self.faq_list_repository.save(faq_list)

            with open(faq_file_import.file_path, 'rt') as fp:
                reader = csv.reader(fp, delimiter=faq_file_import.delimiter)
                # header 読み飛ばし
                next(reader)
                for line in reader:
                    question = line[0]
                    answer = line[1]
                    faq = FaqModel(
                        question=question,
                        question_org=question,
                        answer=answer,
                        answer_org=answer,
                        faq_list_id=faq_list.id)
                    self.faq_repository.save(faq)
        except BaseException as e:
            session.rollback()
            raise e
        finally:
            session.close()

        return True
