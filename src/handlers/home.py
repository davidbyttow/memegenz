import webapp2

from helpers import template_helper


class HomeHandler(webapp2.RequestHandler):
  def get(self):
    html = template_helper.render('index.html')
    self.response.write(html)
