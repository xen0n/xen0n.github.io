#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import markdown2

from . import base
from ..stream import StreamedFile


class MarkdownProcess(base.BaseProcess):
    '''Markdown render pass.'''

    name = 'markdown'

    def __init__(self, prev, options):
        super(MarkdownProcess, self).__init__(prev)

        self.options = options

    def process_file(self, sf):
        content = sf.content.decode('utf-8')
        rendered = markdown2.markdown(content, **self.options)
        return StreamedFile(sf.path, rendered.encode('utf-8'))


# vim:set ai et ts=4 sw=4 sts=4 fenc=utf-8:
