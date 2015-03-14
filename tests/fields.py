import datetime
import jason
import nose
import unittest


class DateTimeFieldTests(unittest.TestCase):
    def setUp(self):
        self.field = jason.fields.DateTimeField()
        self.sample_datetime_string = '2015-03-14T17:30:09'
        self.sample_datetime_object = datetime.datetime(
            year=2015, month=3, day=14, hour=17, minute=30, second=9
        )

    def test_serialization(self):
        """
        Ensure that a datetime object is converted to the right datetime string
        on deserialization.
        """
        self.assertEqual(
            self.field.serialize(self.sample_datetime_object),
            self.sample_datetime_string
        )

    def test_serialization_of_wrong_type(self):
        """
        Ensure that attempting to serialize no-``datetime`` objects raises
        a ``ValidationError``
        """
        self.assertRaises(
            jason.exceptions.ValidationError,
            self.field.serialize,
            10 # An integer cannot be serialized as datetime string
        )

    def test_deserialization(self):
        """
        Ensure that a string is converted to the right datetime object on
        deserialization.
        """
        self.assertEqual(
            self.field.deserialize(self.sample_datetime_string),
            self.sample_datetime_object
        )

    def test_deserialization_of_datetime(self):
        """
        Ensure that attempting to deserialize a datetime object returns the
        object itself, intact
        """
        self.assertEqual(
            self.field.deserialize(self.sample_datetime_object),
            self.sample_datetime_object
        )

    def test_deserialization_of_wrong_string(self):
        """
        Ensure that attempting to deserialize invalid string raises a
        ``ValidationError``
        """
        self.assertRaises(
            jason.exceptions.ValidationError,
            self.field.deserialize,
            'i-am-not-a-date'
        )

    def test_deserialization_of_wrong_type(self):
        """
        Ensure that attempting to deserialize invalid type raises a
        ``ValidationError``
        """
        self.assertRaises(
            jason.exceptions.ValidationError,
            self.field.deserialize,
            9 # A number cannot be converted to a date
        )


class BooleanFieldTests(unittest.TestCase):
    def setUp(self):
        self.field = jason.fields.BooleanField()

    def test_case_insensitive_deserialization_of_true(self):
        """
        Ensure that a string that resolves to ``True`` gets transformed
        properly and case insensitive.
        """
        self.assertEqual(self.field.deserialize('true'), True)
        self.assertEqual(self.field.deserialize('True'), True)
        self.assertEqual(self.field.deserialize('TRUE'), True)

    def test_case_insensitive_deserialization_of_false(self):
        """
        Ensure that a string that resolves to ``False`` gets transformed
        properly and case insensitive.
        """
        self.assertEqual(self.field.deserialize('false'), False)
        self.assertEqual(self.field.deserialize('False'), False)
        self.assertEqual(self.field.deserialize('FALSE'), False)

    def test_case_insensitive_deserialization_of_booleans(self):
        """
        Ensure that attempting to resolve a boolean value works fine
        """
        self.assertEqual(self.field.deserialize(True), True)
        self.assertEqual(self.field.deserialize(False), False)

    def test_case_not_resolvable_string(self):
        """
        Ensure that attempting to resolve a string that does not correspond to
        a boolean value representation, results in raising an ``InvalidData``
        error.
        """
        self.assertRaises(self.field.InvalidData, self.field.deserialize, 'lol')

    def test_case_invalid_type(self):
        """
        Ensure that attempting to resolve an object that is not of str,
        unicode or bool type, results in raising an ``InvalidData`` error.
        """
        self.assertRaises(self.field.InvalidData, self.field.deserialize, 5)


if __name__ == '__main__':
    nose.main()