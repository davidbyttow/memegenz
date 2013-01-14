import base64
import json
import logging
import os
import sys
import webapp2

sys.path.append(os.path.abspath('../model'))

from google.appengine.api import users
from google.appengine.api.images import Image
from google.appengine.ext import db
from helpers import template_helper
from helpers import images
from helpers import sanitize
from helpers.obj import Expando
from model.meme_template import MemeTemplate


def sort_templates(a, b):
  l = a.name.lower()
  r = b.name.lower()
  if l < r:
    return -1
  if l == r:
    return 0
  return 1


class GetTemplatesHandler(webapp2.RequestHandler):
  def get(self):
    req = self.request

    count = int(req.get('count', 75))
    if count > 100:
      count = 100

    q = MemeTemplate.all()
    q.order('-last_used')
    cursor = req.get('cursor')
    if cursor:
      q.with_cursor(cursor)

    templates = []
    for template in q.run(limit=count):
      template_data = Expando({
        'name': template.name,
        'width': template.width,
        'height': template.height
      })
      templates.append(template_data)

    sorted_templates = sorted(templates[:], sort_templates)

    html = template_helper.render('view_templates.html',
      templates=templates,
      alpha_sorted_templates=sorted_templates,
      cursor=q.cursor)
    self.response.write(html)


class CreateTemplateHandler(webapp2.RequestHandler):
  def get(self):
    req = self.request

    html = template_helper.render('upload_template.html')
    self.response.write(html)


class TemplateImageHandler(webapp2.RequestHandler):
  def get(self, template_name):
    req = self.request

    meme_template = MemeTemplate.get_by_key_name(template_name)
    if not meme_template:
      self.error(404)
      return

    self.response.headers['Content-Type'] = 'image/png'
    self.response.headers['Cache-Control'] = 'private, max-age=3600'

    is_thumbnail = req.get('size') == 'thumbnail'
    if is_thumbnail:
      self.response.write(meme_template.thumbnail_image_data)
    else:
      self.response.write(meme_template.image_data)

  def post(self):
    req = self.request

    creator = users.get_current_user().email()
    template_name = sanitize.remove_tags(req.get('template_name'))
    original_image_data = req.get('image_data')

    if not template_name:
      self.error(400)
      return

    existing_template = MemeTemplate.get_by_key_name(template_name)
    if existing_template:
      self.error(400)
      return

    (image_data, width, height) = images.create_image(original_image_data)
    (thumbnail_image_data, _, _) = images.create_thumbnail_image(original_image_data)

    meme_template = MemeTemplate(
      key_name=template_name,
      creator=creator,
      image_data=db.Blob(image_data),
      thumbnail_image_data=db.Blob(thumbnail_image_data),
      name=template_name,
      height=height,
      width=width)
    key = meme_template.put()

    # This should probably redirect to create meme.
    self.redirect('/meme?template_name=' + key.name())


class DeleteTemplateHandler(webapp2.RequestHandler):
  def post(self, template_name):
    req = self.request

    template = MemeTemplate.get_by_key_name(template_name)
    if not template:
      self.error(404)
      return

    if not template.is_owner():
      self.error(400)
      return

    template.delete()

    # Write an empty 200 response
    self.response.headers['Content-Type'] = 'application/json'
    self.response.write('{}')

