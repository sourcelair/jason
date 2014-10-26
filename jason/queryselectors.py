import fields
import re
import requests


class JasonQuerySelector(object):

    class MultipleItemsReturned(Exception):
        pass

    def __init__(self, resource):
        self.resource = resource

    def filter(self, **kwargs):
        url = '%s/%s' % (
            self.resource.service.base_url,
            self.resource.get_root()
        )
        params = {}
        for arg in kwargs:
            field_query_pattern = r'^(\w+)__.+$'
            field_query_search = re.search(field_query_pattern, arg)

            if (field_query_search):
                field = field_query_search.groups()[0]
            else:
                field = arg

            value = kwargs[arg]
            if (hasattr(self.resource, field)):
                attribute = getattr(self.resource, field)
            if (isinstance(attribute, fields.BaseField)):
                value = attribute.__class__(value).deserialize()

            params[arg] = value

        response = requests.get(url, params=params)

        objects = []
        for obj in response.json():
            objects.append(self.resource(obj))
        return objects

    def get(self, **kwargs):
        objects = self.filter(**kwargs)
        if (len(objects) > 1):
            raise self.MultipleItemsReturned
        return objects[0]

    def all(self):
        return self.filter()
