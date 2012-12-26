
from index import IndexHandler
from meme import MemeHandler
from template import TemplateHandler


ROUTES = [
  ('/', IndexHandler),
  ('/meme', MemeHandler),
  ('/template', TemplateHandler),
]
