import logging

from google.appengine.api import images
from google.appengine.api.images import Image


MAX_AREA = 160000
MAX_WIDTH = 800
MAX_HEIGHT = 500
MAX_THUMBNAIL_WIDTH = 314
MAX_THUMBNAIL_HEIGHT = 196

def _resize_image(image_data, max_width, max_height, max_area=0):
  image = Image(image_data=image_data)
  width = image.width
  height = image.height
  aspect = width / float(height)

  if width > max_width:
    width = max_width
    height = width / aspect
  if height > max_height:
    height = max_height
    width = height * aspect

  if max_area > 0:
    area = float(width * height)
    if area > MAX_AREA:
      scalar = MAX_AREA / area
      height *- scalar
      width *= scalar

  height = int(height)
  width = int(width)
  return (images.resize(image_data, width, height, images.PNG),
    width, height)


# Returns a tuple of the form (image_data, width, height)
def create_image(image_data):
  return _resize_image(image_data, MAX_WIDTH, MAX_HEIGHT, MAX_AREA)


def create_thumbnail_image(image_data):
  return _resize_image(image_data, MAX_THUMBNAIL_WIDTH, MAX_THUMBNAIL_HEIGHT)
