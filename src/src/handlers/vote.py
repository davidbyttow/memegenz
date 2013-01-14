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
from helpers import mail
from helpers import template_helper
from helpers.obj import Expando
from model import meme
from model.meme import Meme
from model.meme_template import MemeTemplate


class VoteHandler(webapp2.RequestHandler):
  def get(self, meme_id):
    req = self.request

    voter = users.get_current_user().email()
    voted_meme = meme.vote_for_meme(meme_id, voter)

    # TODO(d): Let others use this.
#    logging.info(voted_meme.creator)
#    if voted_meme and voted_meme.creator == 'd@squareup.com':
#      mail.send_mail_to_user(voted_meme.creator, 'Your meme on the move!',
#        'Someone has voted for your meme: http://memegenz.corp.squareup.com/meme/' + voted_meme.key().name())

    self.redirect('/meme/' + meme_id)


class GetVotersHandler(webapp2.RequestHandler):
  def get(self, meme_id):
    meme = Meme.get_by_key_name(meme_id)
    if not meme:
      self.error(404)
      return

    if not meme:
      self.error(400)
      return

    voters = []
    for voter in meme.voters:
      voters.append(voter.split('@')[0])

    html = template_helper.render('partial/voters.html',
      voters=voters)
    self.response.write(html)
