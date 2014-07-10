from queryselectors import JasonQuerySelector


class JasonResourceMeta(type):
  def __new__(cls, name, bases, dct):
    new_class = type.__new__(cls, name, bases, dct)
    new_class.objects = JasonQuerySelector(new_class)
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
    if (cls.service.root):
      value = '%s/%s' % (cls.service.root, value)
    return value

JasonGenericResource.register_serializer(dict, JasonEmbeddedResource)
