import datetime
from google.appengine.ext import db

class Meme(db.Model):
  creator = db.EmailProperty(required=True, indexed=True)
  create_date = db.DateProperty(required=True, indexed=True, auto_now=True)
  create_datetime = db.DateTimeProperty(required=True, indexed=False, auto_now=True)
  score = db.IntegerProperty(required=True, indexed=False, default=0)
  listed = db.BooleanProperty(indexed=True, default=True)
  width = db.IntegerProperty(required=True, indexed=False)
  height = db.IntegerProperty(required=True, indexed=False)
  image_data = db.BlobProperty(required=True, indexed=False)
