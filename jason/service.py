from resources import JasonResource


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
