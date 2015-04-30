#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from .. import process

import six


def stream_from_config(config):
    '''Instantiate linked processes from a stream config.'''

    return six.moves.reduce(_process_from_config, config, None)


def _process_from_config(sofar, process_decl):
    '''Instantiate a process with the given config.'''

    name, options = process_decl['name'], process_decl.get('args', {})
    return process.get_process(name, options, sofar)


# vim:set ai et ts=4 sw=4 sts=4 fenc=utf-8:
