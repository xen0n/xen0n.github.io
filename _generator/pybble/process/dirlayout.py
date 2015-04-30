#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import pathlib

from . import base
from ..stream import StreamedFile, SkipFile

# TODO: can we make this customizable?
DATE_INDEXED_FILENAME_RE = re.compile(
        r'^(?P<Y>\d{4})'
        r'-(?P<m>\d{2})'
        r'-(?P<d>\d{2})'
        r'-(?P<name>.*)$'
        )


class DirLayoutProcess(base.BaseProcess):
    '''Directory layouting pass.'''

    name = 'dirlayout'

    def __init__(self, prev, skip_unknown=False):
        super(DirLayoutProcess, self).__init__(prev)

        self.skip_unknown = skip_unknown

    def process_file(self, sf):
        match = DATE_INDEXED_FILENAME_RE.match(sf.path.name)

        if match is None:
            # skip or fall through?
            if self.skip_unknown:
                raise SkipFile
            else:
                return sf

        g = match.group
        Y, m, d, basename = g('Y'), g('m'), g('d'), g('name')

        # make directory hierarchy
        path = pathlib.Path(Y) / m / d / basename

        return StreamedFile(path, sf.content)


# vim:set ai et ts=4 sw=4 sts=4 fenc=utf-8:
