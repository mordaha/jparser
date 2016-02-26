#!/usr/bin/env python
# coding: utf8

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import unittest
from jparser import parse_json


class TestJParser(unittest.TestCase):

    def test_parse(self):
        json_line = '{"foo":"bar"}'
        parsed_dict = parse_json(json_line)
        self.assertEqual(parsed_dict['foo'], 'bar')


if __name__ == '__main__':
    unittest.main()
