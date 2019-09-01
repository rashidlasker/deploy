from peewee import *
from models import User, Tweet, db

db.connect()
db.create_tables([User, Tweet])