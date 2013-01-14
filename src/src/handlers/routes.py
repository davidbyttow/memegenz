
from meme import *
from template import *
from user import *
from vote import *


class HelpHandler(webapp2.RequestHandler):
  def get(self):
    html = template_helper.render('what.html')
    self.response.write(html)


ROUTES = [
  webapp2.Route(r'/', handler=GetMemesHandler, name='home'),

  webapp2.Route(r'/meme',
    handler=CreateMemeHandler, name='create-meme'),
  webapp2.Route(r'/meme/delete/<meme_id>',
    handler=DeleteMemeHandler, name='delete-meme'),
  webapp2.Route(r'/meme/image',
    handler=MemeImageHandler, name='create-meme-image'),
  webapp2.Route(r'/meme/image/<meme_id>',
    handler=MemeImageHandler, name='meme-image'),
  webapp2.Route(r'/meme/<meme_id>',
    handler=MemeHandler, name='meme'),
  webapp2.Route(r'/memes',
    handler=GetMemesHandler, name='meme-list'),
  webapp2.Route(r'/stream',
    handler=MemeStreamHandler, name='meme-stream'),
  webapp2.Route(r'/stream/poll',
    handler=MemeStreamPollHandler, name='meme-stream-poll'),

  webapp2.Route(r'/template',
    handler=CreateTemplateHandler, name='create-template'),
  webapp2.Route(r'/template/delete/<template_name>',
    handler=DeleteTemplateHandler, name='delete-template'),
  webapp2.Route(r'/template/image',
    handler=TemplateImageHandler, name='template'),
  webapp2.Route(r'/template/image/<template_name>',
    handler=TemplateImageHandler, name='create-template-image'),
  webapp2.Route(r'/templates',
    handler=GetTemplatesHandler, name='template-list'),

  webapp2.Route(r'/help',
    handler=HelpHandler, name='help'),

  webapp2.Route(r'/me',
    handler=MeHandler, name='me'),
  webapp2.Route(r'/user/<user_name>',
    handler=UserHandler, name='user'),

  webapp2.Route(r'/vote/<meme_id>',
    handler=VoteHandler, name='vote'),
  webapp2.Route(r'/voters/<meme_id>',
    handler=GetVotersHandler, name='votes'),
]
