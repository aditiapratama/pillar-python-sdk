from .resource import List
from .resource import Find
from .resource import Create
from .resource import Post
from .resource import Update
from .resource import Delete
from .resource import Replace
from .exceptions import ResourceNotFound

from . import utils
from .nodes import Node
from .api import Api


class Project(List, Find, Create, Post, Update, Delete, Replace):
    """Project class wrapping the REST nodes endpoint
    """
    path = "projects"

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
        api = api or self.api
        attributes = attributes or self.to_dict()
        etag = attributes['_etag']
        attributes.pop('_id')
        attributes.pop('_etag')
        attributes.pop('_created', None)
        attributes.pop('_updated', None)
        attributes.pop('_links', None)
        attributes.pop('allowed_methods')
        # Remove fields with None value (causes error on validation)
        for prop in ['picture_square', 'picture_header']:
            if prop in attributes and attributes[prop] is None:
                attributes.pop(prop)
            # Strip embedded image file properties and revert to ObjectId
            elif type(attributes[prop]) is dict:
                attributes[prop] = attributes[prop]['_id']
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

    def children(self, api=None):
        api = api or self.api
        children = Node.all({
            'where': '{"project" : "%s", "parent" : {"$exists": false}}'\
                % self._id,
            }, api=api)
        return children

    def get_node_type(self, node_type_name):
        return next((item for item in self.node_types if item.name \
            and item['name'] == node_type_name), None)


    def node_type_has_method(self, node_type_name, method, api=None):
        """Utility method that checks if a given node_type has the requested
        method.
        """
        api = api or Api.Default()
        url = utils.join_url(self.path, str(self._id))
        params = {'projection': '{"permissions":1, "name": 1, "node_types": 1, \
                "url": 1, "user": 1}',
            'node_type': node_type_name}
        url = utils.join_url_params(url, params)
        response = api.get(url)
        node_type = next((item for item in response['node_types'] if item['name'] \
            and item['name'] == node_type_name), None)
        if method in node_type['allowed_methods']:
            return True
        return False


