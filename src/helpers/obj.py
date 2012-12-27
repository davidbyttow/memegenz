

class Expando(dict):
  def __getattr__(self, name):
    return self.__getitem__(name)
