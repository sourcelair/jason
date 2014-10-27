from fields import BaseField
from queryselectors import JasonQuerySelector


class JasonResourceMeta(type):
    def __new__(cls, name, bases, dct):
        new_class = type.__new__(cls, name, bases, dct)

        # Set names to attributes
        for (key, value) in new_class.__dict__.iteritems():
            if (isinstance(value, BaseField)):
                value.name = key

        # Set default query selector
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
    def get_root(cls):
        
        if hasattr(cls, '_root'):
            return cls._root

        value = '%s' % cls.get_resource()

        if cls.service.root:
            value = '%s/%s' % (cls.service.root, value)

        return value
    
    def __unicode__(self):
        repr = (self.__class__.__name__, self.service.base_url)
        return '<%s at %s>' % repr
    
    def __str__(self):
        return self.__unicode__()
    
    def __repr__(self):
        return self.__unicode__()
    

JasonGenericResource.register_serializer(dict, JasonEmbeddedResource)
