#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from ... import driver


def build_cmd(config, args):
    # build stream driver
    stream_driver = driver.StreamDriver.from_config(
            config['streams'],
            callback=(lambda result: (
                print(
                    ' * Stream {} {} in {:.3f} s'.format(
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


# vim:set ai et ts=4 sw=4 sts=4 fenc=utf-8:
