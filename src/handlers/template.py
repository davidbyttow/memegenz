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
from mako.template import Template
from model.meme_template import MemeTemplate


class GetTemplatesHandler(webapp2.RequestHandler):
  def get(self):
    req = self.request

    count = int(req.get('count', 20))
    if count > 100:
      count = 100

    q = MemeTemplate.all().order('-create_datetime')

    cursor = req.get('cursor')
    if cursor:
      q.with_cursor(cursor)

    data = {
      'templates': []
    }

    for template in q.run(limit=count):
      template_data = {
        'name': template.name,
        'width': template.width,
        'height': template.height,
        # TODO(d): I don't think we want to send this down with get templates, instead just
        # individually render the images by calling /template?name=%s with the template name.
#        'image_data': 'data:image/png;base64,' + base64.b64encode(template.image_data),
      }
      data['templates'].append(template_data)

    data['cursor'] = q.cursor()

    self.response.headers['Content-Type'] = 'application/json'
    self.response.write(json.dumps(data))


class TemplateHandler(webapp2.RequestHandler):
  def get(self):
    req = self.request

    # If there's a template id, render it.
    template_name = self.request.get('name')
    if not template_name:
      # TODO(d): Remove this, it should be in the default page handler.
      template = Template(filename='templates/upload_template.html')
      self.response.write(template.render())
      return

    meme_template = MemeTemplate.get_by_key_name(template_name)
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

    existing_template = MemeTemplate.get_by_key_name(template_name)
    if existing_template:
      self.error(400)
      return

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
      key_name=template_name,
      creator=creator,
      image_data=db.Blob(image_data),
      name=template_name,
      height=image.height,
      width=image.width)
    key = meme_template.put()

    # This should probably redirect to create meme.
    self.redirect('/template?name=' + key.name())
