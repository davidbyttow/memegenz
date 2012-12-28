import datetime

from google.appengine.ext import db


class Meme(db.Model):
  creator = db.EmailProperty(required=True, indexed=True)
  create_date = db.DateProperty(required=True, indexed=True, auto_now=True)
  create_datetime = db.DateTimeProperty(required=True, indexed=True, auto_now=True)
  listed = db.BooleanProperty(indexed=True, default=True)
  width = db.IntegerProperty(required=True, indexed=False)
  height = db.IntegerProperty(required=True, indexed=False)
  image_data = db.BlobProperty(required=True, indexed=False)
  template_name = db.StringProperty(required=True, indexed=True)
  voters = db.StringListProperty(default=[])
  score = db.IntegerProperty(indexed=True, default=0)


@db.transactional
def vote_for_meme(meme_id, voter):
  meme = Meme.get_by_id(int(meme_id))
  if not meme:
    return;
  if voter in meme.voters:
    return
  meme.voters.append(voter)
  meme.score = len(meme.voters)
  meme.put()
