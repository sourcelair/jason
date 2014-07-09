from datetime import datetime
import re


class BaseField(object):

  def __init__(self, value=None):
    self._evaluate(value)

  def _is_string(self, value):
    is_string = ((type(value) is str) or (type(value) is unicode))
    return is_string

  def _evaluate(self, value):
    if (value is None):
      self._value = value
      self._string_value = None
      return

    if (self._is_string(value)):
      string_value = value
      value = self.serialize(string_value)
    else:
      string_value = self.deserialize(value)

    self._value = value
    self._string_value = string_value

  def __get__(self, instance, owner):
    return self._value

  def __set__(self, instance, value):
    self._evaluate(value)

  def serialize(self):
    raise NotImplemented()

  def deserialize(self):
    raise NotImplemented()


class DateTimeField(BaseField):

  _pattern = r'^(\d\d\d\d)-(\d\d)-(\d\d)[\sT](\d\d):(\d\d):(\d\d)Z?$'

  def serialize(self, value):
    matches = re.search(self._pattern, value)
    if (matches):
      matches = matches.groups()
      year, month, day, hours, minutes, seconds = (
        int(matches[0]), int(matches[1]), int(matches[2]),
        int(matches[3]), int(matches[4]), int(matches[5])
      )
      return datetime(year, month, day, hours, minutes, seconds)


  def deserialize(self, value):
    pass
