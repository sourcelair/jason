import requests


class JasonResourceQuerySelector(object):

  def __init__(self, resource):
    self.resource = resource

  def all(self):
    url = 'http://%s/%s' % (self.resource.host, self.resource.get_endpoint())
    response = requests.get(url)

    objects = []
    for obj in response.json():
      objects.append(self.resource(obj))
    return objects


class JasonResourceMeta(type):
  def __new__(cls, name, bases, dct):
    new_class = type.__new__(cls, name, bases, dct)
    new_class.objects = JasonResourceQuerySelector(new_class)
    return new_class


class JasonGenericResource(object):

  _serializers = {}

  def __init__(self, data):
    self._data = data

    for key in self._data:
      value = self._data[key]
      value_type = type(value)

      if (value_type in self._serializers):
        value = self._serializers[value_type](value)

      setattr(self, key, value)

  @classmethod
  def register_serializer(cls, object_type, serializer):
    cls._serializers[object_type] = serializer


class JasonEmbeddedResource(JasonGenericResource):
  pass

class JasonResource(JasonGenericResource):

  __metaclass__ = JasonResourceMeta

  @classmethod
  def get_resource(cls):
    return '%ss' % cls.__name__.lower()

  @classmethod
  def get_endpoint(cls):
    value = '%s' % cls.get_resource()
    if (cls.host.root):
      value = '%s/%s' % (cls.host.root, value)
    return value

JasonGenericResource.register_serializer(dict, JasonEmbeddedResource)

class Host(object):

  def __init__(self, host='localhost', root=None):
    self.host = host
    self.root = root

    class Resource(JasonResource):
      host = None
      objects = None

    Resource.host = self

    self.Resource = Resource

  def __unicode__(self):
    return self.host

  def __str__(self):
    return self.__unicode__()
