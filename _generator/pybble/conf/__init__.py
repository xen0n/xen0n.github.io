#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import yaml

DEFAULT_CONFIG_FILENAME = '_pybble.yml'


# http://stackoverflow.com/q/2890146/596531
def construct_yaml_str(self, node):
    return self.construct_scalar(node)


STR_TAG = 'tag:yaml.org,2002:str'
yaml.Loader.add_constructor(STR_TAG, construct_yaml_str)
yaml.SafeLoader.add_constructor(STR_TAG, construct_yaml_str)
del STR_TAG


def load_config(filename=None):
    path = filename if filename is not None else DEFAULT_CONFIG_FILENAME
    with open(path, 'rb') as fp:
        content = fp.read()

    return yaml.load(content)


# vim:set ai et ts=4 sw=4 sts=4 fenc=utf-8:
