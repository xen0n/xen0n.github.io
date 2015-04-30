#!/usr/bin/env python3
# -*- coding: utf-8 -*-

_KNOWN_PROCESSES = {}


def get_process(name, params, prev_process=None):
    return _KNOWN_PROCESSES[name](prev_process, **params)


# let's not bother with auto modprobe for now...
from . import _reg
del _reg


# vim:set ai et ts=4 sw=4 sts=4 fenc=utf-8:
