import jason
import unittest


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
