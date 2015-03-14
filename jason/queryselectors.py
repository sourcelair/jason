import fields
import re
import requests


class JasonQuerySelector(object):

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

        request_kwargs = {
            'params': params
        }

        # Set-up authentication for the request
        if hasattr(self.resource.service, 'auth'):
            auth = self.resource.service.auth
            if callable(auth):
                request_kwargs['auth'] = auth(url, **kwargs)
            else:
                request_kwargs['auth'] = auth

        session = requests.Session()
        request = requests.Request('get', url, **request_kwargs)

        # Apply additional pre-processing (if set)
        if hasattr(self.resource, '_pre_process_request'):
            request = self.resource._pre_process_request(request)

        response = session.send(request.prepare())
        objects = []

        if hasattr(self.resource, '_post_process_response'):
            returned_objects = self.resource._post_process_response(response)
        else:
            returned_objects = response.json()

        for obj in returned_objects:
            objects.append(self.resource(**obj))

        return objects

    def filter(self, **kwargs):
        url = self.resource.get_root()
        return self.query_at(url, **kwargs)

    def get(self, **kwargs):
        objects = self.filter(**kwargs)

        if len(objects) > 1:
            raise self.resource.MultipleItemsReturned

        if len(objects) is 0:
            raise self.resource.NotFound

        return objects[0]

    def all(self):
        return self.filter()
