#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pathlib

from . import base


class DestProcess(base.BaseProcess):
    '''Output process.'''

    name = 'dest'

    def __init__(self, prev, base):
        super(DestProcess, self).__init__(prev)

        self.base = pathlib.Path(base)

    def process_file(self, sf):
        # output into self.base
        dest_path = self.base / sf.path
        print(dest_path)

        # mkdir if necessary
        try:
            # simulate `mkdir -p`
            dest_path.parent.mkdir(parents=True)
        except FileExistsError:
            pass

        # write
        print(repr(sf.content))
        with dest_path.open('wb') as fp:
            fp.write(sf.content)

        return sf


# vim:set ai et ts=4 sw=4 sts=4 fenc=utf-8:
