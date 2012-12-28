import base64
import json
import logging
import os
import sys
import webapp2

sys.path.append(os.path.abspath('../model'))

from google.appengine.api import images
from google.appengine.api import users
from google.appengine.api.images import Image
from google.appengine.ext import db
from helpers import template_helper
from helpers.obj import Expando
from model import meme
from model.meme_template import MemeTemplate


class VoteHandler(webapp2.RequestHandler):
  def get(self, meme_id):
    req = self.request

    voter = users.get_current_user().email()
    meme.vote_for_meme(meme_id, voter)

    self.redirect('/meme/' + meme_id)
