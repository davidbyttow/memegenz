import datetime

from google.appengine.api import users
from google.appengine.ext import db
from helpers.obj import Expando
from helpers import utils


class Meme(db.Model):
  creator = db.EmailProperty(required=True, indexed=True)
  create_date = db.DateProperty(required=True, indexed=True, auto_now_add=True)
  create_datetime = db.DateTimeProperty(required=True, indexed=True, auto_now_add=True)
  listed = db.BooleanProperty(indexed=True, default=True)
  width = db.IntegerProperty(required=True, indexed=False)
  height = db.IntegerProperty(required=True, indexed=False)
  image_data = db.BlobProperty(required=True, indexed=False)
  thumbnail_image_data = db.BlobProperty(required=True, indexed=False)
  template_name = db.StringProperty(required=True, indexed=True)
  voters = db.StringListProperty(default=[])
  score = db.IntegerProperty(indexed=True, default=0)
  text = db.StringProperty(indexed=True, multiline=True)

  def create_data(self):
    meme_data = Expando({
      'author': utils.make_user_name(self.creator),
      'is_owner': self.is_owner(),
      'id': self.key().name(),
      'width': self.width,
      'height': self.height,
      'score': self.score,
    })
    return meme_data

  def is_owner(self):
    user_email = users.get_current_user().email()
    return self.creator == user_email


@db.transactional
def vote_for_meme(meme_id, voter):
  meme = Meme.get_by_key_name(meme_id)
  if not meme:
    return;
  if voter in meme.voters:
    return
  meme.voters.append(voter)
  meme.score = len(meme.voters)
  meme.put()
