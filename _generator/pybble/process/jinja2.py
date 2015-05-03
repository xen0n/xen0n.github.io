#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re

import jinja2

from . import base
from ..stream import StreamedFile


class Jinja2Process(base.BaseProcess):
    '''Jinja2 render pass.

    Returns non-virtual files.

    '''

    name = 'jinja2'

    def __init__(self, prev, template_dir, env):
        super(Jinja2Process, self).__init__(prev)

        self.template_dir = template_dir

        jinja_env = jinja2.Environment(
                loader=jinja2.FileSystemLoader([template_dir, ], 'utf-8'),
                auto_reload=False,
                )
        jinja_env.globals = env
        self._env = jinja_env

    def process_file(self, sf):
        template_name = '{0}.html'.format(sf.attrs['layout'])
        template = self._env.get_template(template_name)

        context = {
            'post': sf,
            }
        rendered = template.render(context).encode('utf-8')

        # use .html as suffix
        out_path = sf.path.with_suffix('.html')
        return StreamedFile(out_path, rendered, sf.attrs, False)


# vim:set ai et ts=4 sw=4 sts=4 fenc=utf-8:
