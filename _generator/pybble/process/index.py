#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from . import base
from ..stream import StreamedFile


def post_object_from_sf(sf):
    tmp = sf.attrs.copy()
    del tmp['layout']

    # assumes dirlayout-processed path; like `yyyy/mm/dd/index.md`
    tmp['path'] = sf.path.parent

    return tmp


class IndexProcess(base.BaseProcess):
    '''Index generation pass.

    Buffers all of input; aggregates all files with attribute ``layout`` set to
    ``post``, writing to attribute of the index page (whose `layout`` is
    ``index``.)

    '''

    name = 'index'
    anticausal = True

    def __init__(self, prev):
        super(IndexProcess, self).__init__(prev)

    def process_buffered(self, files):
        # XXX: a little bit of mutable state is ok?
        index_file = None
        posts_indexed = []

        for sf in files:
            layout = sf.attrs.get('layout', '')

            if layout == 'index':
                # mark for later modification...
                index_file = sf
                continue

            if layout == 'post':
                # time-descending order
                posts_indexed.append((-sf.attrs.get('date').timestamp(), sf, ))

        posts_indexed.sort()
        post_objs = [post_object_from_sf(post) for _, post in posts_indexed]
        index_file.attrs['posts'] = post_objs

        return files


# vim:set ai et ts=4 sw=4 sts=4 fenc=utf-8:
