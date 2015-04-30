#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from . import base
from ..stream import source


class SourceProcess(base.BaseProcess):
    '''Globber-based source process.'''

    name = 'src'

    def __init__(self, prev, path, cwd='.'):
        super(SourceProcess, self).__init__(prev)

        self.globber = source.Globber(path, cwd)

    def stream_source(self):
        return self.globber.stream()


# vim:set ai et ts=4 sw=4 sts=4 fenc=utf-8:
