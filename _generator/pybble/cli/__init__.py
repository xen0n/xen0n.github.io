#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from .. import conf
from .. import driver


def main(argv):
    '''CLI Entrypoint.'''

    # use default config for now
    config = conf.load_config(None)

    # build stream processes
    stream = driver.stream_from_config(config['stream'])

    # let's stream!
    stream.run()

    return 0


# vim:set ai et ts=4 sw=4 sts=4 fenc=utf-8:
