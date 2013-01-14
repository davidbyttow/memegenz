
import random


ALPHA = 'abcdefghijklmnopqrstuvwxyz'
ALPHA_LEN = len(ALPHA)


def randomString(numChars):
  str = ''
  for i in range(numChars):
    v = int(random.random() * (ALPHA_LEN * ALPHA_LEN) % ALPHA_LEN)
    str += ALPHA[v]
  return str
