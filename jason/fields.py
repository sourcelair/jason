from datetime import datetime
import re


class BaseField(object):

    name = None

    class InvalidData(Exception):
        """
        Should be raised, when invalid data is passed to the fied for
        serialization or deserialization.
        """
        pass

    def __init__(self, value=None, query_field=None):
        self._evaluate(value)
        self._query_field = query_field

    def _is_string(self, value):
        is_string = ((type(value) is str) or (type(value) is unicode))
        return is_string

    def _evaluate(self, value):
        if (self._is_string(value)):
            self._value = self.serialize(value)
        else:
            self._value = value

    def __get__(self, instance, owner):
        if (instance is None):
            return self
        return self.serialize(instance._data.get(self.name))

    def __set__(self, instance, value):
        self._evaluate(value)

    def serialize(self, value):
        return value

    def deserialize(self):
        return self._value

    def __unicode__(self):
        return self.deserialize()

    def __str__(self):
        return self.__unicode__()


class StringField(BaseField):
    pass


class IntegerField(BaseField):
    def serialize(self, value):
        return int(value)

    def deserialize(self):
        return str(self._value)


class DateTimeField(BaseField):

    _pattern = r'^(\d\d\d\d)-(\d\d)-(\d\d)[\sT](\d\d):(\d\d):(\d\d)'

    def serialize(self, value):
        matches = re.search(self._pattern, value)
        if (matches):
            matches = matches.groups()
            year, month, day, hour, minute, seconds = (
                int(matches[0]), int(matches[1]), int(matches[2]),
                int(matches[3]), int(matches[4]), int(matches[5])
            )
        return datetime(year, month, day, hour, minute, seconds)


    def deserialize(self):
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
    def serialize(self, value):
        # Attempt to match case-insensitive string with True
        if re.match(r'^true$', value, re.IGNORECASE):
            return True
        # Attempt to match case-insensitive string with False
        if re.match(r'^false$', value, re.IGNORECASE):
            return False
        # Let the user know that the given value cannot be serialized into
        # boolean
        err = 'Value "%s" of type "%s", could not be serialized into boolean'
        err = err % (value, type(value))
        raise self.InvalidData(err)

    def deserialize(self):
        if self._value:
            return 'true'
        else:
            return 'false'
