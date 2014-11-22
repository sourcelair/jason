import fields
import re
import requests


class JasonQuerySelector(object):

    class MultipleItemsReturned(Exception):
        pass

    def __init__(self, resource):
        self.resource = resource

    def query_at(self, url, **kwargs):
        params = {}

        for arg in kwargs:
            field_query_pattern = r'^(\w+)__.+$'
            field_query_search = re.search(field_query_pattern, arg)

            if field_query_search:
                field = field_query_search.groups()[0]
            else:
                field = arg

            value = kwargs[arg]

            if hasattr(self.resource, field):
                attribute = getattr(self.resource, field)

            if isinstance(attribute, fields.BaseField):
                field_instance = attribute.__class__(value)
                value = field_instance.deserialize()

                if attribute._query_field:
                    arg = attribute._query_field

            params[arg] = value

        response = requests.get(url, params=params)
        objects = []

        for obj in response.json():
            objects.append(self.resource(**obj))

        return objects

    def filter(self, **kwargs):
        url = self.resource.get_root()
        return self.query_at(url, **kwargs)

    def get(self, **kwargs):
        objects = self.filter(**kwargs)
        if (len(objects) > 1):
            raise self.MultipleItemsReturned
        return objects[0]

    def all(self):
        return self.filter()
