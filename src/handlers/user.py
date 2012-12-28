import logging
import os
import sys
import webapp2

sys.path.append(os.path.abspath('../model'))

from model import meme
from model.meme import Meme

from google.appengine.api import images
from google.appengine.api import users
from google.appengine.api.images import Image
from google.appengine.ext import db
from helpers import template_helper
from helpers.obj import Expando


def is_dev_mode():
  return os.environ['SERVER_SOFTWARE'].startswith('Development')

def make_user_email(user_name):
  if user_name.find('@') != -1:
    return user_name
  if is_dev_mode():
    return user_name + '@example.com'
  return user_name + '@squareup.com'


def make_user_name(user_email):
  return user_email.split('@')[0]


class MeHandler(webapp2.RequestHandler):
  def get(self):
    self.redirect('/user/' + make_user_name(users.get_current_user().email()))


class UserHandler(webapp2.RequestHandler):
  def get(self, user_name):
    req = self.request

    count = int(req.get('count', 20))
    if count > 100:
      count = 100

    # TODO(d): Super hack.
    user_email = make_user_email(user_name)

    q = Meme.all().order('-score').filter('creator', user_email)

    cursor = req.get('cursor')
    if cursor:
      q.with_cursor(cursor)

    memes = []
    for meme in q.run(limit=count):
      meme_data = Expando({
        'author': user_name,
        'id': meme.key().id(),
        'width': meme.width,
        'height': meme.height,
        'score': meme.score,
      })
      memes.append(meme_data)

    html = template_helper.render('view_memes.html', memes=memes)
    self.response.write(html)
