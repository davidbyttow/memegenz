import sys
import os
sys.path.append(os.path.abspath('../model'))
from model.meme import Meme
import webapp2

from google.appengine.api import images
from google.appengine.api import users
from google.appengine.api.images import Image
from helpers import template_helper
from helpers.obj import Expando


class GetMemesHandler(webapp2.RequestHandler):
  def get(self):
    req = self.request

    memes = Expando()

    # TODO(d): finish this

    html = template_helper.render('view_memes.html', memes=memes)
    self.response.write(html)


class CreateMemeHandler(webapp2.RequestHandler):
  def get(self):
    req = self.request

    html = template_helper.render('create_meme.html')
    self.response.write(html)


class MemeHandler(webapp2.RequestHandler):
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

    # Create the image and transform it to a PNG.
    image = Image(image_data=image_data)
    if (image.width > 800):
      scalar = 800 / image.width
      image.resize(800, image.height * scalar)
    image.execute_transforms(output_encoding=images.PNG)

    meme = Meme(
      creator=creator,
      listed=listed,
      image_data=db.Blob(image),
      template_name=template_name,
      height=image.height,
      width=image.width)
    key = meme.put()

    self.redirect('/meme/' + str(key.id()))

  # TODO(d): redirect to viewing the meme

  def delete(self):
    req = self.request

    # TODO(d): delete the meme if the user has permission
