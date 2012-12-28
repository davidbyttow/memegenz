
from home import *
from meme import *
from template import *
from user import *
from vote import *


ROUTES = [
  webapp2.Route(r'/', handler=GetMemesHandler, name='home'),

  webapp2.Route(r'/meme',
    handler=CreateMemeHandler, name='create-meme'),
  webapp2.Route(r'/meme/<meme_id:\d+>',
    handler=MemeHandler, name='meme'),
  webapp2.Route(r'/meme/image/<meme_id:\d+>',
    handler=MemeImageHandler, name='meme'),
  webapp2.Route(r'/memes',
    handler=GetMemesHandler, name='meme'),

  webapp2.Route(r'/template',
    handler=CreateTemplateHandler, name='create-template'),
  webapp2.Route(r'/template/image/<template_name>',
    handler=TemplateImageHandler, name='template'),
  webapp2.Route(r'/templates',
    handler=GetTemplatesHandler, name='template-list'),

  webapp2.Route(r'/me',
    handler=MeHandler, name='me'),
  webapp2.Route(r'/user/<user_name>',
    handler=UserHandler, name='user'),

  webapp2.Route(r'/vote/<meme_id:\d+>',
    handler=VoteHandler, name='vote'),
]
