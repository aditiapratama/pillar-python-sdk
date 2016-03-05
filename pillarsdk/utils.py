import re
from datetime import datetime

try:
    from urllib.parse import urlencode
except ImportError:
    from urllib import urlencode


def join_url(url, *paths):
    """
    Joins individual URL strings together, and returns a single string.

    Usage::

        >>> utils.join_url("pillar:5000", "shots")
        pillar:5000/shots
    """
    for path in paths:
        url = re.sub(r'/?$', re.sub(r'^/?', '/', path), url)
    return url


def join_url_params(url, params):
    """Constructs a query string from a dictionary and appends it to a url.

    Usage::

        >>> utils.join_url_params("pillar:5000/shots", {"page-id": 2, "NodeType": "Shot Group"})
        pillar:5000/shots?page-id=2&NodeType=Shot+Group
    """
    return url + "?" + urlencode(params)


def merge_dict(data, *override):
    """
    Merges any number of dictionaries together, and returns a single dictionary.

    Usage::

        >>> utils.merge_dict({"foo": "bar"}, {1: 2}, {"foo1": "bar2"})
        {1: 2, 'foo': 'bar', 'foo1': 'bar2'}
    """
    result = {}
    for current_dict in (data,) + override:
        result.update(current_dict)
    return result


def convert_datetime(item):
    """Starting from a JSON object, find and replace the _create and _updated
    keys with actual datetime objects.
    """
    keys = ['_updated', '_created']

    for k in keys:
        item[k] = datetime.strptime(item[k], "%a, %d %b %Y %H:%M:%S %Z")

    return item


def remove_none_attributes(attributes):
    """Return a new dict with all None values removed"""
    # out = {}
    # for k, v in attributes.iteritems():
    #     if v is not None:
    #         if type(v) is dict:
    #             attributes[k] = remove_none_attributes(v)
    #         else:
    #             out[k] = v
    # return out

    if isinstance(attributes, (list, tuple, set)):
        return type(attributes)(remove_none_attributes(x) for x in attributes if x is not None)
    elif isinstance(attributes, dict):
        return type(attributes)((remove_none_attributes(k), remove_none_attributes(v))
            for k, v in attributes.items() if k is not None and v is not None)
    else:
        return attributes
