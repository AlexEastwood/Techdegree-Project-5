from peewee import *
from flask_login import UserMixin
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
        
    def get_tags(self):
        return (
            Tag.select().join(
                EntryTags, on=EntryTags.tag
            ).where(
                EntryTags.entry == self
            )
        )
        

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
        
    @classmethod
    def create_entry(cls, tag_name):
        try:
            with DATABASE.transaction():
                cls.create(
                    tag_name=tag_name)
        except IntegrityError:
            raise ValueError("Entry already exists")

class EntryTags(Model):
    entry = ForeignKeyField(Entry)
    tag = ForeignKeyField(Tag)
    
    class Meta:
        database = DATABASE
        
class User(UserMixin, Model):
    user_id = AutoField()
    username = CharField(unique=True)
    password = CharField()
    
    class Meta:
        database = DATABASE
        
    def get_id(self):
           return (self.user_id)
        
    @classmethod
    def create_user(cls, username, password):
        try:
            with DATABASE.transaction():
                cls.create(
                    username=username,
                    password=password
                )
        except IntegrityError:
            raise ValueError("User already exists")

def initialize():
    DATABASE.connect()
    DATABASE.create_tables([Entry, Tag, EntryTags, User], safe=True)
    DATABASE.close()
