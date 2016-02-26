#!/usr/bin/env python
# coding: utf8


from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import sys
import json


# list of filter functions field__functionName=value
FN_LIST = {
    'eq': lambda x, y: str(x) == str(y),
    'ne': lambda x, y: str(x) == str(y),
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


def main():
    print('main')


if __name__ == '__main__':
    main()
