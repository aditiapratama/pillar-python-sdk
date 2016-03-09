from .resource import List
from .resource import Find
from .resource import Create
from .resource import Post
from .resource import Update
from .resource import Delete
from .resource import Replace
from .exceptions import ResourceNotFound

from . import utils
from .api import Api


class Node(List, Find, Create, Post, Update, Delete, Replace):
    """Node class wrapping the REST nodes endpoint
    """
    path = "nodes"

    @classmethod
    def find_one(cls, params, api=None):
        """Get one resource starting from parameters different than the resource
        id. TODO if more than one match for the query is found, raise exception.
        """
        api = api or Api.Default()

        # Force delivery of only 1 result
        params['max_results'] = 1
        url = utils.join_url_params(cls.path, params)

        response = api.get(url)
        # Keep the response a dictionary, and cast it later into an object.
        if response['_items']:
            item = utils.convert_datetime(response['_items'][0])
            return cls(item)
        else:
            raise ResourceNotFound(response)

    def update(self, attributes=None, api=None):
        def pop_none_attributes(attributes):
            """Return a new dict with all None values removed"""
            out = {}
            for k, v in attributes.iteritems():
                if v:
                    if type(v) is dict:
                        attributes[k] = pop_none_attributes(v)
                    else:
                        out[k] = v
            return out

        api = api or self.api
        attributes = attributes or self.to_dict()
        etag = attributes['_etag']
        attributes.pop('_id')
        attributes.pop('_etag')
        attributes.pop('_created')
        attributes.pop('_updated')
        attributes.pop('_links', None)
        attributes.pop('allowed_methods')
        # for attr in ['parent', 'picture']:
        #     if attr in attributes and attributes[attr] is None:
        #         attributes.pop(attr, None)
        pop_none_attributes(attributes)

        url = utils.join_url(self.path, str(self['_id']))
        headers = utils.merge_dict(
            self.http_headers(),
            {'If-Match': str(etag)})
        new_attributes = api.put(url, attributes, headers)
        self.error = None
        self.merge(new_attributes)
        return self.success()

    def has_method(self, method):
        if method in self.allowed_methods:
            return True
        return False


class NodeType(List, Find, Create, Post, Delete):
    """NodeType class wrapping the REST node_types endpoint
    """
    path = "node_types"

    def has_method(self, method):
        if method in self.allowed_methods:
            return True
        return False
