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
from helpers import utils


class MeHandler(webapp2.RequestHandler):
  def get(self):
    self.redirect('/user/' + utils.make_user_name(users.get_current_user().email()))


class UserHandler(webapp2.RequestHandler):
  def get(self, user_name):
    req = self.request

    count = int(req.get('count', 20))
    if count > 100:
      count = 100

    # TODO(d): Super hack.
    user_email = utils.make_user_email(user_name)

    q = Meme.all().order('-score').filter('creator', user_email)

    cursor = req.get('cursor')
    if cursor:
      q.with_cursor(cursor)

    memes = []
    for meme in q.run(limit=count):
      memes.append(meme.create_data())

    page_title = user_name + '\'s Memes'

    html = template_helper.render('view_memes.html',
      page_title=page_title,
      memes=memes)
    self.response.write(html)
