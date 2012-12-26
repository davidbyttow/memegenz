
from index import *
from meme import *
from template import *
from editor import *


ROUTES = [
  ('/', IndexHandler),
  ('/meme', MemeHandler),
  ('/editor', EditorHandler),
  ('/template', TemplateHandler),
  ('/templates', GetTemplatesHandler),
]
