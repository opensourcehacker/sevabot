# -*- coding: utf-8 -*-
"""

    Module loader

"""


from __future__ import absolute_import, division, print_function, unicode_literals

import os
import logging
import threading
import subprocess

import settings

logger = logging.getLogger("sevabot")

#: Module name -> executable mappings
_modules = {}


def load_modules():
    """
    Scan all modules folders for executable scripts.
    """

    _modules.clear()

    for folder in settings.MODULE_PATHS:
        folder = os.path.abspath(folder)
        for f in os.listdir(folder):
            fpath = os.path.join(folder, f)

            # Remove file extension
            body, ext = os.path.splitext(f)

            if os.access(fpath, os.X_OK):
                logger.info("Discovered module %s: %s" % (body, fpath))
                _modules[body] = fpath

    if not len(_modules.keys()):
        raise RuntimeError("No modules found in: %s" % settings.MODULE_PATHS)

    return _modules.keys()


def is_module(name):
    """
    Check if a named module exists.
    """
    return name in _modules


def run_module(name, args, callback):
    """
    Run an external script asynchronously.

    Timeout with a message if the default threshold is reached.
    """
    logger.debug("Executing module %s: %s" % (name, args))

    #timeout(execute_module, name, args, callback, default=)

    default = "Module %s timeouted in %d seconds" % (name, settings.TIMEOUT)

    def run():
        """
        Execute external command, capture output.
        """
        args.insert(0, unicode(_modules[name]))

        logger.debug("Running command line: %s" % " ".join(args))

        process = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=False)
        out = process.communicate()[0]

        # :E1103: *%s %r has no %r member (but some types could not be inferred)*
        # pylint: disable=E1103
        return out.decode("utf-8")

    thread = ExecutionManagedThread(run, default, settings.TIMEOUT, callback)
    thread.start()


class ExecutionManagedThread(threading.Thread):
    """
    A thread which will wait the actual task thread.join()
    """
    def __init__(self, func, default, timeout, callback):
        threading.Thread.__init__(self)
        self.result = default
        self.func = func
        self.callback = callback
        self.default = default
        self.timeout = timeout

    def run(self):
        runner = ExecutionThread(self.func)
        runner.start()
        runner.join(self.timeout)

        if runner.isAlive():
            logger.warn("Timeouted running external command")
            return self.callback(self.default)
        else:
            return self.callback(runner.result)


class ExecutionThread(threading.Thread):
    """
    Run any function.
    """
    def __init__(self, func):
        threading.Thread.__init__(self)
        self.result = None
        self.func = func

    def run(self):
        self.result = self.func()


