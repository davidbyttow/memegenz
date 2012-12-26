
from home import *
from meme import *
from template import *
from editor import *


ROUTES = [
  webapp2.Route(r'/', handler=HomeHandler, name='home'),

  webapp2.Route(r'/meme', handler=CreateMemeHandler, name='create-meme'),
  webapp2.Route(r'/meme/<meme_id:\d+>', handler=MemeHandler, name='meme'),

  webapp2.Route(r'/template', handler=CreateTemplateHandler, name='create-template'),
  webapp2.Route(r'/template/<template_name>', handler=TemplateHandler, name='template'),
  webapp2.Route(r'/templates', handler=GetTemplatesHandler, name='template-list'),
]
