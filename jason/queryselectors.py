import requests


class JasonQuerySelector(object):

  class MultipleItemsReturned(Exception):
    pass

  def __init__(self, resource):
    self.resource = resource

  def filter(self, **kwargs):
    url = 'http://%s/%s' % (self.resource.service, self.resource.get_endpoint())
    response = requests.get(url, params=kwargs)

    objects = []
    for obj in response.json():
      objects.append(self.resource(obj))
    return objects

  def get(self, **kwargs):
    objects = self.filter(**kwargs)
    if (len(objects) > 1):
      raise self.MultipleItemsReturned
    return objects[0]

  def all(self):
    return self.filter()
