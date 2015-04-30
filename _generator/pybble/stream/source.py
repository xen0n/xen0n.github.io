#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pathlib

from . import StreamedFile


class Globber(object):
    '''Provider of streamed files.'''

    def __init__(self, pattern, cwd):
        self.pattern = pattern
        self.cwd = cwd

    def stream(self):
        base = pathlib.Path(self.cwd)
        for path in base.glob(self.pattern):
            with path.open('rb') as fp:
                content = fp.read()

            yield StreamedFile(path.relative_to(base), content)


# vim:set ai et ts=4 sw=4 sts=4 fenc=utf-8:
