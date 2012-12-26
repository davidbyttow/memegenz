import datetime

from google.appengine.ext import db


class MemeTemplate(db.Model):
  creator = db.EmailProperty(required=True, indexed=True)
  create_datetime = db.DateTimeProperty(required=True, indexed=False, auto_now=True)
  name = db.StringProperty(required=True, indexed=False)
  width = db.IntegerProperty(required=True, indexed=False)
  height = db.IntegerProperty(required=True, indexed=False)
  image_data = db.BlobProperty(required=True, indexed=False)
