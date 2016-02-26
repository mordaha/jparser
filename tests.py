#!/usr/bin/env python
# coding: utf8

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import unittest

from jparser import parse_json, format_line, filter_line, parse_filter_string


class TestJParser(unittest.TestCase):
    def setUp(self):
        self.json_line = '{"@fields": {"uuid": "92c4c7cc-f00c-4c77-bc71-3687d33c225d", "level": "INFO", "status_code": 200, "content_type": "application/json", "path": "/v1/items/1/", "method": "PUT", "name": "django.http"}, "@timestamp": "2015-12-15T05:45:39+00:00", "@source_host": "c57872949172", "@message": "Request processed"}'

    def test_parse_json(self):
        parsed_dict = parse_json(self.json_line)
        self.assertIsInstance(parsed_dict['@fields'], dict)
        self.assertEqual(parsed_dict['@source_host'], 'c57872949172')

    def test_format_line(self):
        parsed_dict = parse_json(self.json_line)
        sss = format_line("[{@timestamp}] {@fields[level]} {@message}", **parsed_dict)
        self.assertEqual(sss, '[2015-12-15T05:45:39+00:00] INFO Request processed')

    def test_parse_filter_string(self):
        parsed_dict = parse_json(self.json_line)
        keys, fn, val = parse_filter_string(' @fields.level = INFO ')

        self.assertEqual(keys, ['@fields', 'level'])

    def test_filter(self):
        parsed_dict = parse_json(self.json_line)
        keys, fn, val = parse_filter_string(' @fields.level = INFO ')
        result = filter_line(keys, fn, val, **parsed_dict)
        self.assertEqual(result, True)

        keys, fn, val = parse_filter_string(' @fields.level = ZZZ ')
        result = filter_line(keys, fn, val, **parsed_dict)
        self.assertEqual(result, False)


if __name__ == '__main__':
    unittest.main()
