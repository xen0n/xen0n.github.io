#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse

from .. import conf
from .. import driver

parser = argparse.ArgumentParser(
        description='Pybble command-line interface.',
        )

parser.add_argument('-c', dest='config', help='Config file to use')

subparsers = parser.add_subparsers(
        title='sub-commands')

parser_build = subparsers.add_parser(
        'build',
        help='Build the specified project',
        )


def build_cmd(config, args):
    # build stream driver
    stream_driver = driver.StreamDriver.from_config(
            config['streams'],
            callback=(lambda result: (
                print(
                    ' * Stream {} {} in {} s'.format(
                        result['stream_name'],
                        'completed' if not result['exception'] else 'errored',
                        result['time_end'] - result['time_start'],
                        )),
                (print(result['exception']) if result['exception'] else 0),
                ))
            )

    # let's stream!
    stream_driver.execute()

    return 0


parser_build.set_defaults(func=build_cmd)


def main():
    '''CLI Entrypoint.'''

    args = parser.parse_args()
    config = conf.load_config(args.config)

    if not hasattr(args, 'func'):
        parser.print_usage()
        return 1

    return args.func(config, args)


# vim:set ai et ts=4 sw=4 sts=4 fenc=utf-8:
