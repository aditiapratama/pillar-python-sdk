# -*- encoding: utf-8 -*-

import datetime
import json
import unittest

try:
    from urllib.parse import quote_plus
except ImportError:
    # Python 2
    from urllib import quote_plus

from pillarsdk import utils
from pillarsdk.resource import Resource


class PillarUtilsTests(unittest.TestCase):
    def test_join_url_params(self):
        """Test that strings and dicts work as parameters."""

        # Test empty and None parameters
        self.assertEqual('?', utils.join_url_params('', {}))
        self.assertEqual('url', utils.join_url_params('url', None))

        # Test simple string values
        self.assertEqual('url?param=simple_param', utils.join_url_params('url', {'param': 'simple_param'}))
        self.assertEqual('url?param=space+param', utils.join_url_params('url', {'param': 'space param'}))

        # Test dictionary
        self.assertEqual('url?dict=' + quote_plus('{"key": "value"}'),
                         utils.join_url_params('url', {'dict': {'key': 'value'}}))

        # Test nested dictionary
        self.assertEqual('url?dict=' + quote_plus('{"key": {"subkey": "subvalue"}}'),
                         utils.join_url_params('url', {'dict': {'key': {'subkey': 'subvalue'}}}))

    def test_join_url_params_encoding(self):
        """Test that unicode objects in the query parameters are properly UTF-8 encoded."""

        # Test simple unicode string
        self.assertEqual('url?param=St%C3%BCvel', utils.join_url_params('url', {'param': u'Stüvel'}))

        # Test unicode value in string
        self.assertEqual('url?dict=' + quote_plus(r'{"food": "\u0e1c\u0e31\u0e14\u0e44\u0e17\u0e22"}'),
                         utils.join_url_params('url', {'dict': {'food': 'ผัดไทย'}}))

    def test_join_url_params_sorting(self):
        # Different sorting than in the tests before, and using multiple keys per dict so
        # that sorting is actually relevant.
        self.assertEqual('url?after=haha+actually+before' +
                         '&dict=' + quote_plus(r'{"drinks": "water", "food": "\u0e1c\u0e31\u0e14\u0e44\u0e17\u0e22"}') +
                         '&last=yeah%2C+last',
                         utils.join_url_params('url', {'dict': {'food': 'ผัดไทย', 'drinks': 'water'},
                                                       'after': 'haha actually before',
                                                       'last': 'yeah, last'}))

    def test_merge_dict(self):
        self.assertEqual({1: 2, 'foo': 'bar', 'foo1': 'bar2'},
                         utils.merge_dict({"foo": "bar"}, {1: 2}, {"foo1": "bar2"}))

        self.assertEqual({'foo': 'bar'}, utils.merge_dict({'foo': 'bar'}, None))

        self.assertEqual({'foo': 'bar'}, utils.merge_dict(None, {'foo': 'bar'}))
        self.assertEqual({}, utils.merge_dict(None, None))

    def test_json_encoding(self):
        resource = Resource()
        resource['datetime'] = datetime.datetime(2016, 3, 22, 12, 35, 16)

        as_json = json.dumps(resource, cls=utils.PillarJSONEncoder, sort_keys=True)
        self.assertEqual('{"datetime": "2016-03-22 12:35:16"}', as_json)

    def test_sanitize_filename(self):

        self.assertEqual('abc.def', utils.sanitize_filename('abc.def'))
        self.assertEqual('abc.def', utils.sanitize_filename('. . abc.def . . '))
        self.assertEqual('abc......def', utils.sanitize_filename('././abc../..///..def'))
        self.assertEqual('Pad Thai is ผัดไทย', utils.sanitize_filename('Pad Thai is ผัดไทย'))
        self.assertEqual(u'Pad Thai is ผัดไทย', utils.sanitize_filename(u'Pad Thai is ผัดไทย'))
