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

    def serialize(self, value):
        raise NotImplementedError()

    def __unicode__(self):
        return self.serialize(self._value)

    def __str__(self):
        return self.__unicode__()


class StringField(BaseField):
    def deserialize(self, value):
        return value

    def serialize(self, value):
        return value


class IntegerField(BaseField):
    def deserialize(self, value):
        return int(value)

    def serialize(self, value):
        return str(value)


class DateTimeField(BaseField):
    """
    Implements jason field for serializing and deserializing datetime values.
    """

    # Matches strings in the following form 2015-03-14T19:49:59
    _pattern = r'^(\d\d\d\d)-(\d\d)-(\d\d)[\sT](\d\d):(\d\d):(\d\d)'

    def deserialize(self, value):
        if isinstance(value, datetime):
            return value
        elif not self._is_string(value):
            err = 'Object of %s type cannot be deserialized to datetime'
            err = err % type(value)
            raise exceptions.ValidationError(err)

        matches = re.search(self._pattern, value)
        if (matches):
            matches = matches.groups()
            year, month, day, hour, minute, seconds = (
                int(matches[0]), int(matches[1]), int(matches[2]),
                int(matches[3]), int(matches[4]), int(matches[5])
            )
            return datetime(year, month, day, hour, minute, seconds)
        err = 'The given string cannot be resolved to a datetime object'
        raise exceptions.ValidationError(err)


    def serialize(self, value):
        if not isinstance(value, datetime):
            err = 'The given is not datetime, thus it cannot be serialized'
            raise exceptions.ValidationError(err)

        year = value.year
        month = value.month
        day = value.day
        # Be less strict from now on
        if hasattr(value, 'hour'):
            hour = value.hour
        else:
            hour = 0
        if hasattr(value, 'minute'):
            minute = value.minute
        else:
            minute = 0
        if hasattr(value, 'second'):
            second = value.second
        else:
            second = 0
        value = '%d-%02d-%02dT%02d:%02d:%02d' % (
            year, month, day, hour, minute, second
        )
        return value


class BooleanField(BaseField):
    """
    Implements jason field for serializing and desirializing boolean values.
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

    def serialize(self, value):
        if self._value:
            return 'true'
        else:
            return 'false'
