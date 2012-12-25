import webapp2, os, logging
from google.appengine.ext.webapp import template

class MainHandler(webapp2.RequestHandler):
  def get(self):
    self.response.headers['Content-Type'] = 'text/html'
    self.response.write('Hello, World!')

class EditorHandler(webapp2.RequestHandler):
  def get(self):
    logging.info("editor")
    
    self.response.headers['Content-Type'] = 'text/html'
    self.response.write('Hello, World!')
    
    #template_values = {}
    #path = os.path.join(os.path.dirname(__file__), 'templates/editor.html')
    #logging.info("template path: %s", path)
    #self.response.out.write(template.render(path, template_values))

app = webapp2.WSGIApplication(
  [ 
    ('/', MainHandler),
    ('/editor', EditorHandler),
  ],
  debug=True)
