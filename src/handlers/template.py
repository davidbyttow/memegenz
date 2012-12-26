import model
import webapp2

from google.appengine.api import images


class TemplateHandler(webapp2.RequestHandler):
  def post(self):
    req = self.request

    creator = users.get_current_user().email()
    name = req.get('name')
    width = req.get('width')
    height = req.get('height')
    image_data = req.get('image_data')

    meme_template = model.MemeTemplate()
    meme_template.creator = creator
    meme_template.listed = listed
    meme_template.image_data = image_data
    meme_template.template_name = template_name
    meme_template.height = height
    meme_template.width = width
    meme_template.put()