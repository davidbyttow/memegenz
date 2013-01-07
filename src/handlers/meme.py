import os
import sys
sys.path.append(os.path.abspath('../model'))

import base64
import datetime
import json
import logging
import re
import user
import webapp2

from google.appengine.api import users
from google.appengine.api.images import Image
from google.appengine.ext import db
from helpers import template_helper
from helpers import images
from helpers import randoms
from helpers import utils
from helpers.obj import Expando
from model import meme
from model.meme import Meme
from model.meme_template import MemeTemplate


DATA_URL_PATTERN = re.compile('data:image/(png|jpeg);base64,(.*)$')


def generate_meme_key_name():
  key_name = randoms.randomString(5)
  while Meme.get_by_key_name(key_name):
    key_name = randoms.randomString(5)
  return key_name


def insert_meme(creator, listed, template_name, original_image_data, text):
  (image_data, width, height) = images.create_image(original_image_data)
  (thumbnail_image_data, _, _) = images.create_thumbnail_image(original_image_data)

  key_name = generate_meme_key_name()

  meme = Meme(
    key_name=key_name,
    creator=creator,
    listed=listed,
    image_data=db.Blob(image_data),
    thumbnail_image_data=db.Blob(thumbnail_image_data),
    template_name=template_name,
    text=text,
    height=height,
    width=width)
  return meme.put()


class GetMemesHandler(webapp2.RequestHandler):
  def get(self):
    req = self.request

    count = int(req.get('count', 20))
    if count > 100:
      count = 100

    q = Meme.all()

    page_title = ''
    order = req.get('order')
    if order == 'recent':
      q.order('-create_datetime')
      page_title = 'Recent'
    else:
      q.order('-create_date').order('-score')
      page_title = 'Top'

    q.filter('listed', True)
    template_name = req.get('template_name')
    if template_name:
      page_title += ' ' + template_name
      q.filter('template_name', template_name)
    cursor = req.get('cursor')
    if cursor:
      q.with_cursor(cursor)

    page_title += ' Memes'

    memes = []
    for meme in q.run(limit=count):
      memes.append(meme.create_data())

    html = template_helper.render('view_memes.html',
      page_title=page_title,
      memes=memes)
    self.response.write(html)


class CreateMemeHandler(webapp2.RequestHandler):
  def get(self):
    req = self.request

    template_name = req.get('template_name')
    if not template_name:
      self.error(400)
      return

    html = template_helper.render('create_meme.html')
    self.response.write(html)


class MemeHandler(webapp2.RequestHandler):
  def get(self, meme_id):
    req = self.request

    meme = Meme.get_by_key_name(meme_id)
    if not meme:
      self.error(404)
      return

    author_name = utils.make_user_name(meme.creator)
    meme_data = meme.create_data()

    page_title = meme.template_name + ' Meme by ' + author_name
    html = template_helper.render('view_meme.html',
      page_title=page_title,
      meme=meme_data)
    self.response.write(html)


class MemeImageHandler(webapp2.RequestHandler):
  def get(self, meme_id):
    req = self.request

    # If there's a meme id, render it.
    # TODO(d): Guard against non-integer ids
    meme = Meme.get_by_key_name(meme_id)
    if not meme:
      self.error(404)
      return

    self.response.headers['Content-Type'] = 'image/png'
    self.response.headers['Cache-Control'] = 'public, max-age=86400'

    is_thumbnail = req.get('size') == 'thumbnail'
    if is_thumbnail:
      self.response.write(meme.thumbnail_image_data)
    else:
      self.response.write(meme.image_data)

  def post(self):
    req = self.request

    data_url = req.get('image_data')
    if not data_url:
      self.error(400)
      return

    bottom_text = req.get('upper_text')
    upper_text = req.get('lower_text')
    texts =[]
    if bottom_text:
      texts.append(bottom_text)
    if upper_text:
      texts.append(upper_text)
    text = '\n'.join(texts)

    encoded_image_data = DATA_URL_PATTERN.match(data_url).group(2)
    if encoded_image_data is None or len(encoded_image_data) == 0:
      self.error(400)
      return

    image_data = base64.b64decode(encoded_image_data)

    creator = users.get_current_user().email()
    listed = req.get('listed') == 'true'

    template_name = req.get('template_name')

    key = insert_meme(creator, listed, template_name, image_data, text)

    meme_template = MemeTemplate.get_by_key_name(template_name)
    if meme_template:
      meme_template.last_used = datetime.datetime.now()
      meme_template.put()

    data = {
      'id': key.name()
    }
    self.response.headers['Content-Type'] = 'application/json'
    self.response.write(json.dumps(data))

class DeleteMemeHandler(webapp2.RequestHandler):
  def post(self, meme_id):
    req = self.request

    # If there's a meme id, render it.
    # TODO(d): Guard against non-integer ids
    meme = Meme.get_by_key_name(meme_id)
    if not meme:
      self.error(404)
      return

    if not meme.is_owner():
      self.error(400)
      return

    meme.delete()

    # Write an empty 200 response
    self.response.headers['Content-Type'] = 'application/json'
    self.response.write('{}')

