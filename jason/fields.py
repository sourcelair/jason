from datetime import datetime
import exceptions
import re
import resources


class BaseField(object):

    name = None

    class InvalidData(Exception):
        """
        Should be raised, when invalid data is passed to the fied for
        serialization or deserialization.
        """
        pass

    def __init__(self, value=None, query_field=None, required=False):
        self._evaluate(value)
        self.query_field = query_field
        self.required = required

    def _is_string(self, value):
        is_string = ((type(value) is str) or (type(value) is unicode))
        return is_string

    def _evaluate(self, value):
        if self._is_string(value):
            self._value = self.deserialize(value)
        else:
            self._value = value

    def __get__(self, instance, owner):
        instance_is_jason_resource = isinstance(
            instance, resources.JasonGenericResource
        )
        # If this field is accessed using the class, or if it does not belong
        # to a Jason Resource, then return itself, else return its
        # deserialized representation
        if instance is None or not instance_is_jason_resource:
            return self
        else:
            value = instance._data.get(self.name)
            # In any case do not attempt to deserialize ``None``
            if value is None:
                # If this field is None and required, then raise a validation
                # error
                if self.required:
                    raise exceptions.ValidationError
                else:
                    return None
            return self.deserialize(value)

    def __set__(self, instance, value):
        self._evaluate(value)

    def deserialize(self, value):
        raise NotImplementedError()

    def serialize(self):
        raise NotImplementedError()

    def __unicode__(self):
        return self.serialize()

    def __str__(self):
        return self.__unicode__()


class StringField(BaseField):
    def deserialize(self, value):
        return value

    def serialize(self):
        return self._value


class IntegerField(BaseField):
    def deserialize(self, value):
        return int(value)

    def serialize(self):
        return str(self._value)


class DateTimeField(BaseField):

    _pattern = r'^(\d\d\d\d)-(\d\d)-(\d\d)[\sT](\d\d):(\d\d):(\d\d)'

    def deserialize(self, value):
        matches = re.search(self._pattern, value)
        if (matches):
            matches = matches.groups()
            year, month, day, hour, minute, seconds = (
                int(matches[0]), int(matches[1]), int(matches[2]),
                int(matches[3]), int(matches[4]), int(matches[5])
            )
        return datetime(year, month, day, hour, minute, seconds)


    def serialize(self):
        if (self._value is None):
              return None
        value = '%d-%02d-%02dT%02d:%02d:%02d' % (self._value.year,
                                                 self._value.month,
                                                 self._value.day,
                                                 self._value.hour,
                                                 self._value.minute,
                                                 self._value.second)
        return value


class BooleanField(BaseField):
    """
    Implements field for serializing and desirializing boolean values.
    """
    def deserialize(self, value):
        if type(value) is bool:
            return value
        elif type(value) in [str, unicode]:
            # Attempt to match case-insensitive string with True
            if re.match(r'^true$', value, re.IGNORECASE):
                return True
            # Attempt to match case-insensitive string with False
            if re.match(r'^false$', value, re.IGNORECASE):
                return False
        # Let the user know that the given value cannot be deserialized into
        # boolean
        err = 'Value "%s" of type "%s", could not be deserialized into boolean'
        err = err % (value, type(value))
        raise self.InvalidData(err)

    def serialize(self):
        if self._value:
            return 'true'
        else:
            return 'false'
