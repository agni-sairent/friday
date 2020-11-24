import sys

from services.DatabaseService import DatabaseService
from models.Homework import Homework
from models.Subject import Subject
from models.Work import Work
from models.Note import Note

db = DatabaseService().get_db()


def prepare_db():
    db.create_tables([Homework, Subject, Work, Note])
    return True


print(prepare_db())
sys.exit(0)

