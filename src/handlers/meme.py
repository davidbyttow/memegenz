import sys
import os
sys.path.append(os.path.abspath('../model'))
from model.meme import Meme
import webapp2

from google.appengine.api import images
from google.appengine.api import users
from google.appengine.api.images import Image
from mako.template import Template


class GetUserMemesHandler(webapp2.RequestHandler):
  def get(self):
    req = self.request

    creator = req.get('email')
    if not creator:
      self.error(400)
      return

    count = int(req.get('count', 20))
    if count > 100:
      count = 100

    # TODO(d): finish this


class MemeHandler(webapp2.RequestHandler):
  def get(self):
    req = self.request

    # If there's a meme id, render it.
    id = self.request.get('id')
    if not id:
      self.error(400)
      return

    # TODO(d): Guard against non-integer ids
    meme = MemeTemplate.get_by_id(int(id))
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

  # TODO(d): redirect to viewing the meme

  def delete(self):
    req = self.request

    # TODO(d): delete the meme if the user has permission
