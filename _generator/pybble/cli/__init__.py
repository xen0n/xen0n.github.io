#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse

from .. import conf
from .commands import build

parser = argparse.ArgumentParser(
        description='Pybble command-line interface.',
        )

parser.add_argument('-c', dest='config', help='Config file to use')

subparsers = parser.add_subparsers(
        title='sub-commands')

# TODO: refactor this into subcommand module
parser_build = subparsers.add_parser(
        'build',
        help='Build the specified project',
        )
parser_build.set_defaults(func=build.build_cmd)


def main():
    '''CLI Entrypoint.'''

    args = parser.parse_args()
    config = conf.load_config(args.config)

    if not hasattr(args, 'func'):
        parser.print_usage()
        return 1

    return args.func(config, args)


# vim:set ai et ts=4 sw=4 sts=4 fenc=utf-8:
