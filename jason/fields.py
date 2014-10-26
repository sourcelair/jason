from datetime import datetime
import re


class BaseField(object):

    name = None

    def __init__(self, value=None):
        self._evaluate(value)

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
