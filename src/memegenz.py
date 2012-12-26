import webapp2

from handlers import routes


app = webapp2.WSGIApplication(
  routes.ROUTES,
  debug=True)
