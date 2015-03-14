class NotFound(Exception):
    """
    This Exception should be raised, when the user queries an API and gets a
    404 response.
    """
    pass


class MultipleItemsReturned(Exception):
    """
    This Exception should be raised, when the user queries an API for one
    Resource, but more than one are returned.
    """
    pass


class ValidationError(Exception):
    """
    This Exception should be raised when a Jason Model fails validation.
    """
    pass

