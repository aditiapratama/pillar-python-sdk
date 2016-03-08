# -*- encoding: utf-8 -*-

import unittest

try:
    from urllib.parse import quote_plus
except ImportError:
    # Python 2
    from urllib import quote_plus

from pillarsdk import utils


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
