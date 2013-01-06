
import logging
import os
import sys
import time

from google.appengine.api import users


def is_dev_mode():
  return os.environ['SERVER_SOFTWARE'].startswith('Development')

def make_user_email(user_name):
  if user_name.find('@') != -1:
    return user_name
  if is_dev_mode():
    return user_name + '@example.com'
  return user_name + '@squareup.com'


def make_user_name(user_email):
  return user_email.split('@')[0]


def make_timestamp(datetime):
  return int(time.mktime(datetime.timetuple()) * 1000)
