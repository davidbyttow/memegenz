import model
import webapp2

from google.appengine.api import images


class MemeHandler(webapp2.RequestHandler):
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
    width = req.get('width')
    height = req.get('height')

    meme = model.Meme()
    meme.creator = creator
    meme.listed = listed
    meme.image_data = image_data
    meme.template_name = template_name
    meme.height = height
    meme.width = width
    meme.put()