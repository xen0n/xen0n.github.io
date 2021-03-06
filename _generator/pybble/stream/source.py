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
            if not path.is_file():
                # we're not interested in directories or broken symlinks
                continue

            with path.open('rb') as fp:
                content = fp.read()

            yield StreamedFile(path.relative_to(base), content, {}, False)


# vim:set ai et ts=4 sw=4 sts=4 fenc=utf-8:
