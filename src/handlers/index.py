import webapp2

from mako.template import Template


class IndexHandler(webapp2.RequestHandler):
  def get(self):
    template = Template(filename='templates/index.html')
    self.response.write(template.render(person='Jason'))
