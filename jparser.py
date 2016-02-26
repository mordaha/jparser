#!/usr/bin/env python
# coding: utf8


from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import sys
import os
import json
import argparse
import fileinput


DEFAULT_FORMAT = '[{@timestamp}] {@fields[level]} {@message}'

# list of test functions field__functionName=value
# x is val from filter, y is value from json line
FN_LIST = {
    'eq': lambda x, y: str(x) == str(y),
    'ne': lambda x, y: str(x) != str(y),
    'in': lambda x, y: str(y) in str(x),
}


def parse_filter_string(s):
    """
    parses strink like "key1.key2.key3__fn=val"
      and returns tuple:
        ([list of keys], fn from FN_LIST or FN_LIST['eq'], val)
    """
    left, val = s.strip().split('=')
    val = val.strip()

    assert val

    try:
        left, fn_str = left.strip().split('__')
        fn_str = fn_str.strip()
    except ValueError:
        fn_str = 'eq'

    if not fn_str or fn_str not in FN_LIST.keys():
        fn_str = 'eq'

    fn = FN_LIST[fn_str]

    keys = left.strip().split('.')
    # keys = map(lambda x: x.strip(), keys)

    return keys, fn, val


def filter_line(keys, fn, val, **kwargs):
    """
    checks if kwargs contains key1.ke2.key3 (from keys) value
    and returns result of fn(val, value) check, fn from FN_LIST
    """
    search_value = kwargs
    for key in keys:
        # may use .get() to avoid KeyError
        search_value = search_value[key]
    return fn(search_value, val)


def format_line(format_string, **kwargs):
    return format_string.format(**kwargs)


def parse_json(json_line):
    return json.loads(json_line)


def main(input_buff, output_buff, argv):
    """
    reads format and filters from argv
    reads lines from input_buff by .readline()
    parses json
    checks parsed_dict against filters
    if passed writes formatted line to output_buff
    """
    parser = argparse.ArgumentParser('It is all about parsing json...')
    parser.add_argument('--format',
                        help='as for string.format() default is "{}"'.format(DEFAULT_FORMAT),
                        default=DEFAULT_FORMAT)
    parser.add_argument('--filter', action='append', help='e.g. key.key.key__fn=val')
    args = parser.parse_args(argv)

    filters = args.filter or []
    format_string = args.format
    filters_parsed = map(parse_filter_string, filters)

    while True:
        line = input_buff.readline()
        if not line:
            break

        parsed_dict = parse_json(line.strip())
        #
        # this way Too complicated to read :)
        #
        # # if more than 1 filter given - tests parsed_dict against each with 'and' logic
        # filter_pass = reduce(
        #     lambda acc, x: acc and x,
        #     map(
        #         # x is (keys, fn, val) tuples as returned by parse_filter_string()
        #         lambda x: filter_line(*x, **parsed_dict),
        #         filters_parsed
        #     ),
        #     True)

        filter_pass = True
        for filter_tuple in filters_parsed:
            filter_pass = filter_pass and filter_line(*filter_tuple, **parsed_dict)
            if not filter_pass:
                break

        if filter_pass:
            output_buff.write(format_line(format_string, **parsed_dict))
            output_buff.write("\n")


if __name__ == '__main__':
    main(sys.stdin, sys.stdout, sys.argv[1:])
