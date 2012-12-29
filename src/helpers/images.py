
from google.appengine.api import images
from google.appengine.api.images import Image


MAX_AREA = 160000
MAX_WIDTH = 800
MAX_HEIGHT = 500

# Returns a tuple of the form (image_data, width, height)
def resize_image(image_data):
  image = Image(image_data=image_data)
  width = image.width
  height = image.height
  aspect = width / height

  if width > MAX_WIDTH:
    width = MAX_WIDTH
    height = width / aspect
  if height > MAX_HEIGHT:
    height = MAX_HEIGHT
    width = height * aspect

  area = width * height
  if area > MAX_AREA:
    scalar = MAX_AREA / area

  return (images.resize(image_data, width, height, images.PNG),
    width, height)
