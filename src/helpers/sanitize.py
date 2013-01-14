

SPECIAL_CHARS = [
  ('<', ''),
  ('>', ''),
  ('&', ''),
]
  

def remove_tags(string):
  # Ultra simple tag replacement.
  for group in SPECIAL_CHARS:
    string = string.replace(group[0], group[1])
  return string
