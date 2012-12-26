import sys
import os
sys.path.append(os.path.abspath('../model'))
from model.meme import Meme
import webapp2

from google.appengine.api import images
from google.appengine.api import users
from google.appengine.api.images import Image
from mako.template import Template

class EditorHandler(webapp2.RequestHandler):
  def get(self):
    template = Template(filename='templates/editor.html')
    self.response.write(template.render())