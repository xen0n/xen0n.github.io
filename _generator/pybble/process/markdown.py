#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re

import markdown2
import yaml

from . import base
from ..stream import StreamedFile

FILE_HEADER_RE = re.compile(r'(?s)^---\n(.*)\n---\n')


class PreMarkdownProcess(base.BaseProcess):
    '''Preprocessing pass for Markdown.

    Implements Jekyll-like file header processing. Also decodes input file with
    UTF-8 for rendering.

    '''

    name = 'markdown-pre'

    def process_file(self, sf):
        content = sf.content.decode('utf-8')
        match = FILE_HEADER_RE.match(content)

        if match is None:
            # pass through
            return StreamedFile(sf.path, content, sf.attrs, True)

        # load attrs
        attached_attrs = yaml.load(match.group(1))
        new_attrs = sf.attrs.copy()
        new_attrs.update(attached_attrs)

        # strip the file content of header
        stripped_content = content[match.end():]

        return StreamedFile(sf.path, stripped_content, new_attrs, True)


class MarkdownProcess(base.BaseProcess):
    '''Markdown render pass.

    Returns virtual files.

    '''

    name = 'markdown'

    def __init__(self, prev, options):
        super(MarkdownProcess, self).__init__(prev)

        self.options = options

    def process_file(self, sf):
        rendered = markdown2.markdown(sf.content, **self.options)

        result = {
            'content': rendered,
            }
        return StreamedFile(sf.path, result, sf.attrs, True)


# vim:set ai et ts=4 sw=4 sts=4 fenc=utf-8:
