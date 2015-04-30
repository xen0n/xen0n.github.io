#!/usr/bin/env python3
# -*- coding: utf-8 -*-


class StreamedFile(object):
    '''Streamed file.'''

    def __init__(self, path, content, attrs, virtual):
        self.path = path
        self.content = content
        self.attrs = attrs
        self.virtual = virtual


class SkipFile(Exception):
    '''Exception to raise to skip the currently processed StreamedFile.'''

    pass


# vim:set ai et ts=4 sw=4 sts=4 fenc=utf-8:
