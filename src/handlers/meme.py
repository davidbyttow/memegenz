import logging
import os
import sys
import webapp2

sys.path.append(os.path.abspath('../model'))

from model import meme
from model.meme import Meme
from model.meme_template import MemeTemplate

from google.appengine.api import images
from google.appengine.api import users
from google.appengine.api.images import Image
from google.appengine.ext import db
from helpers import template_helper
from helpers.obj import Expando


def insert_meme(creator, listed, template_name, image_data):
  # Create the image and transform it to a PNG.
  image = Image(image_data=image_data)
  width = image.width
  height = image.height
  if (image.width > 800):
    width = 800
    height = image.height * scalar
  image_data = images.resize(image_data, width, height, images.PNG)

  meme = Meme(
    creator=creator,
    listed=listed,
    image_data=db.Blob(image_data),
    template_name=template_name,
    height=image.height,
    width=image.width)
  return meme.put()


class GetMemesHandler(webapp2.RequestHandler):
  def get(self):
    req = self.request

    count = int(req.get('count', 20))
    if count > 100:
      count = 100

    q = Meme.all()

    order = req.get('order')
    if order == 'recent':
      q.order('-create_datetime')
    else:
      q.order('-create_date').order('-score')

    cursor = req.get('cursor')
    if cursor:
      q.with_cursor(cursor)

    memes = []
    for meme in q.run(limit=count):
      meme_data = Expando({
        'author': meme.creator,
        'id': meme.key().id(),
        'width': meme.width,
        'height': meme.height,
        'score': meme.score,
      })
      memes.append(meme_data)

    html = template_helper.render('view_memes.html', memes=memes)
    self.response.write(html)


class CreateMemeHandler(webapp2.RequestHandler):
  def get(self):
    req = self.request

    template_name = req.get('template_name')
    if not template_name:
      self.error(400)
      return

    # TODO(d): This entire next block is for testing only until the editor is ready
    forced = req.get('forced')
    if forced:
      meme_template = MemeTemplate.get_by_key_name(template_name)
      if not meme_template:
        self.error(400)
        return
      image_data = meme_template.image_data
      logging.info('raw: ' + image_data)
      key = insert_meme(
        users.get_current_user().email(), True, template_name, image_data)
      self.redirect('/meme/' + str(key.id()))
      return

    html = template_helper.render('create_meme.html')
    self.response.write(html)


class MemeHandler(webapp2.RequestHandler):
  def get(self, meme_id):
    req = self.request

    meme = Meme.get_by_id(int(meme_id))
    if not meme:
      self.error(404)
      return

    meme_data = Expando({
      'author': meme.creator,
      'id': meme_id,
      'width': meme.width,
      'height': meme.height,
      'score': meme.score,
    })

    html = template_helper.render('view_meme.html', meme=meme_data)
    self.response.write(html)


class MemeImageHandler(webapp2.RequestHandler):
  def get(self, meme_id):
    req = self.request

    # If there's a meme id, render it.
    # TODO(d): Guard against non-integer ids
    meme = Meme.get_by_id(int(meme_id))
    if not meme:
      self.error(404)
      return

    self.response.headers['Content-Type'] = 'image/png'
    self.response.write(meme.image_data)

  def post(self):
    req = self.request

    creator = users.get_current_user().email()
    listed = req.get('listed', False)
    if listed:
      listed = True
    else:
      listed = False

    template_name = req.get('template_name')
    image_data = req.get('image_data')

    key = insert_meme(creator, listed, template_name, image_data)
    self.redirect('/meme/image/' + str(key.id()))

  def delete(self):
    req = self.request

    # TODO(d): delete the meme if the user has permission
