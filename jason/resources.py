from fields import BaseField
from queryselectors import JasonQuerySelector
import exceptions


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

    NotFound = exceptions.NotFound
    MultipleItemsReturned = exceptions.MultipleItemsReturned

    _serializers = {}

    def __init__(self, **data):
        """
        Initialize a new Jason resource with arbitrary data.
        """
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
    def __init__(self, dict_obj):
        # Take care of edge case
        if 'self' in dict_obj:
            dict_obj['_self'] = dict_obj['self']
            del dict_obj['self']
        super(JasonEmbeddedResource, self).__init__(**dict_obj)


class JasonResource(JasonGenericResource):

    __metaclass__ = JasonResourceMeta

    @classmethod
    def get_root(cls):
        
        if hasattr(cls, '_root'):
            return cls._root

        value = '%ss' % cls.__name__.lower()

        if cls.service.root:
            value = '%s/%s' % (cls.service.base_url, value)

        return value
    
    def __unicode__(self):
        repr = (self.__class__.__name__, self.service.base_url)
        return '<%s at %s>' % repr
    
    def __str__(self):
        return self.__unicode__()
    
    def __repr__(self):
        return self.__unicode__()
    

JasonGenericResource.register_serializer(dict, JasonEmbeddedResource)
