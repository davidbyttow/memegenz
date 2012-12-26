
from index import *
from meme import *
from template import *


ROUTES = [
  ('/', IndexHandler),
  ('/meme', MemeHandler),
  ('/template', TemplateHandler),
  ('/templates', GetTemplatesHandler),
]
