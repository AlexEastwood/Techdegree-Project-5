from peewee import *

import datetime

DATABASE = SqliteDatabase("journal.db")


class Entry(Model):
    entry_id = AutoField()
    title = CharField(unique=True)
    date = DateField(default=datetime.datetime.now)
    time_spent = IntegerField()
    learned = TextField()
    resources = TextField()

    class Meta:
        database = DATABASE

    @classmethod
    def create_entry(cls, title, time_spent, learned, resources):
        try:
            with DATABASE.transaction():
                cls.create(
                    title=title,
                    time_spent=time_spent,
                    learned=learned,
                    resources=resources
                    )
        except IntegrityError:
            raise ValueError("Entry already exists")


def initialize():
    DATABASE.connect()
    DATABASE.create_tables([Entry], safe=True)
    DATABASE.close()
