from resources import JasonResource
import re


class Service(object):

    def __init__(self, host='localhost', root=None):
        self.host = host
        self.root = root

        class Resource(JasonResource):
            host = None
            objects = None

        Resource.service = self
        self.Resource = Resource

    def __unicode__(self):
        return self.host

    def __str__(self):
        return self.__unicode__()

    @property
    def base_url(self):
        _base_url = self.host
        
        if not re.match(r'^https?://', _base_url):
            _base_url = 'http://%s' % _base_url
        
        if (self.root):
            _base_url = '%s/%s' % (_base_url, self.root)

        return _base_url