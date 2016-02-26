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


# list of filter functions field__functionName=value
FN_LIST = {
    'eq': lambda x, y: str(x) == str(y),
    'ne': lambda x, y: str(x) != str(y),
    'like': lambda x, y: str(y) in str(x),
}


def parse_filter_string(s):
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
    search_value = kwargs
    for key in keys:
        # здесь можно сделать .get() чтобы ингорировать несуществующие ключи
        search_value = search_value[key]
    return fn(search_value, val)


def format_line(format_string, **kwargs):
    return format_string.format(**kwargs)


def parse_json(json_line):
    return json.loads(json_line)


def main(input_buff, *argv):
    def hook_nobuf(filename, mode):
        return open(filename, mode, 0)

    parser = argparse.ArgumentParser('It is all about parsing json...')
    parser.add_argument('--format', default='[{@timestamp}] {@fields[level]} {@message}')
    parser.add_argument('--filter', action='append')
    args = parser.parse_args(argv)

    filters = args.filter or []
    format_string = args.format
    filters_parsed = map(parse_filter_string, filters)

    while True:
        line = input_buff.readline().strip()
        if not line:
            break

        parsed_dict = parse_json(line)

        # if more than 1 filter given - tests parsed_dict against each with 'and' logic
        filter_pass = reduce(
            lambda acc, x: acc and x,
            map(
                # x is (keys, fn, val) tuples as returned by parse_filter_string()
                lambda x: filter_line(*x, **parsed_dict),
                filters_parsed
            ),
            True)

        if filter_pass:
            print(format_line(format_string, **parsed_dict))


if __name__ == '__main__':
    main(sys.stdin, *sys.argv[1:])
