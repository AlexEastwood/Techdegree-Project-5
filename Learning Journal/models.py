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
        
class Tag(Model):
    tag_name = CharField(unique=True)
    
    class Meta:
        database = DATABASE

class EntryTags(Model):
    entry = ForeignKeyField(Entry)
    tag = ForeignKeyField(Tag)
    
    class Meta:
        database = DATABASE

def initialize():
    DATABASE.connect()
    DATABASE.create_tables([Entry, Tag, EntryTags], safe=True)
    DATABASE.close()
