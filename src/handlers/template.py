import logging
import os
import sys
import webapp2

sys.path.append(os.path.abspath('../model'))

from google.appengine.api import images
from google.appengine.api import users
from google.appengine.api.images import Image
from google.appengine.ext import db
from mako.template import Template
from model.meme_template import MemeTemplate


class TemplateHandler(webapp2.RequestHandler):
  def get(self):
    req = self.request

    id = self.request.get('id')
    if not id:
      template = Template(filename='templates/upload_template.html')
      self.response.write(template.render())
      return

    meme_template = MemeTemplate.get_by_id(int(id))
    if not meme_template:
      self.error(404)
      return

    self.response.headers['Content-Type'] = 'image/png'
    self.response.write(meme_template.image_data)

  def post(self):
    req = self.request

    creator = users.get_current_user().email()
    template_name = req.get('template_name')
    image_data = req.get('image_data')

    # Create an image in order to get the width and height
    image = Image(image_data=image_data)
    width = image.width
    height = image.height
    if (image.width > 800):
      width = 800
      height = image.height * scalar
    else:
      image.resize(image.width, image.height)
    image_data = images.resize(image_data, width, height, images.PNG)

    meme_template = MemeTemplate(
      creator=creator,
      image_data=db.Blob(image_data),
      name=template_name,
      height=image.height,
      width=image.width)
    key = meme_template.put()

    self.redirect('/template?id=' + str(key.id()))
