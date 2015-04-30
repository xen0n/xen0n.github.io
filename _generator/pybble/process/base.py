#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import six

from . import _KNOWN_PROCESSES
from ..stream import SkipFile


class MetaProcess(type):
    '''Metaclass for auto-registering process classes.'''

    def __new__(cls, name, bases, attrs):
        new_cls = super(MetaProcess, cls).__new__(cls, name, bases, attrs)

        proc_name = new_cls.name

        # hack to allow BaseProcess itself
        if name == 'BaseProcess':
            return new_cls

        if proc_name is None:
            raise TypeError('name is required for processes')

        if not isinstance(proc_name, six.text_type):
            raise TypeError('name must be text')

        _KNOWN_PROCESSES[proc_name] = new_cls

        return new_cls


@six.add_metaclass(MetaProcess)
class BaseProcess(object):
    '''Base class for process passes.'''

    name = None

    def __init__(self, prev):
        self.prev = prev

    def run(self):
        '''Process a stream of StreamedFiles.'''
        return list(self.run_iter())

    def run_iter(self):
        if self.prev is None:
            # we're source
            for sf in self.stream_source():
                yield sf

            return

        # stream from the previous process
        for sf in self.prev.run_iter():
            try:
                yield self.process_file(sf)
            except SkipFile:
                # skip this file
                pass

    def process_file(self, sf):
        # base impl does nothing
        return sf

    def stream_source(self):
        '''Provide the stream source if asked to be the source process.'''

        # base impl returns empty iterable
        return []


# vim:set ai et ts=4 sw=4 sts=4 fenc=utf-8:
