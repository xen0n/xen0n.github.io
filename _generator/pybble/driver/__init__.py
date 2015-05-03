#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from .. import process

import six
import threading
import time
import queue


def stream_from_config(config):
    '''Instantiate linked processes from a stream config.'''

    return six.moves.reduce(_process_from_config, config, None)


def _process_from_config(sofar, process_decl):
    '''Instantiate a process with the given config.'''

    name, options = process_decl['name'], process_decl.get('args', {})
    return process.get_process(name, options, sofar)


class StreamDriverThread(threading.Thread):
    def __init__(self, process, stream_name, result_queue):
        super(StreamDriverThread, self).__init__(
                name='StreamDriver-{}'.format(stream_name)
                )

        self.stream_name = stream_name
        self.process = process
        self.result_queue = result_queue

    def run(self):
        time_start = time.time()
        self.process.run()
        time_end = time.time()

        result = {
                'stream_name': self.stream_name,
                'time_start': time_start,
                'time_end': time_end,
                }
        self.result_queue.put(result)


class StreamDriver(object):
    '''Stream driver driving one or more streams.'''

    def __init__(self, streams, callback=None):
        self.streams = streams
        self.callback = callback

    @classmethod
    def from_config(cls, config, **kwargs):
        streams = [stream_from_config(stream_decl) for stream_decl in config]
        return cls(streams, **kwargs)

    def execute(self):
        nb_streams = len(self.streams)
        result_queue = queue.Queue(nb_streams)
        threads = [
                StreamDriverThread(process, str(idx), result_queue)
                for idx, process in enumerate(self.streams)
                ]

        for thread in threads:
            thread.start()

        for i in range(nb_streams):
            result = result_queue.get()
            if self.callback is not None:
                self.callback(result)

        # this shouldn't be necessary but do it anyway
        for thread in threads:
            thread.join()


# vim:set ai et ts=4 sw=4 sts=4 fenc=utf-8:
