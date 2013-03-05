# -*- coding: utf-8 -*-
"""

    Module loader

"""


from __future__ import absolute_import, division, print_function, unicode_literals

import os
import logging
import threading
import subprocess
import imp

import settings

logger = logging.getLogger("sevabot")

#: Module name -> executable mappings
_modules = {}


def fail_safe(func):
    """
    Python decorator to make sure we don't let exceptions slip through.

    We log all exceptions to logging output.
    """

    def closure(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except Exception as e:
            logger.exception(e)

    return closure


class UNIXScriptModule:
    """ Simple UNIX script file wrapper"""

    def __init__(self, name, path):
        self.path = path
        self.name = name

    def shutdown(self):
        pass

    @staticmethod
    def is_valid(path):
        """ Is this a module we are looking for """
        return os.access(path, os.X_OK)

    def run_module(self, args, callback):
        """
        Run an external script asynchronously.

        Timeout with a message if the default threshold is reached.
        """
        logger.debug("Executing module %s: %s" % (self.name, args))

        #timeout(execute_module, name, args, callback, default=)
        def run():
            args.insert(0, unicode(self.name))

            logger.debug("Running command line: %s" % " ".join(args))

            process = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=False)
            out = process.communicate()[0]

            # :E1103: *%s %r has no %r member (but some types could not be inferred)*
            # pylint: disable=E1103
            return out.decode("utf-8")

        default = "Module %s timeouted in %d seconds" % (self.name, settings.TIMEOUT)

        thread = ExecutionManagedThread(run, default, settings.TIMEOUT, callback)
        thread.start()


class StatefulModule:
    """ State maintaining module.

    The module is a reloadable Python file with

    - #!/sevabot magic string at the head of the file

    - Exports Python attribute *sevabot_handler* which is an instance

    """
    def __init__(self, skype, name, path):
        self.path = path
        self.name = name
        self.init(skype)

    @staticmethod
    def is_valid(path):
        """ Is this a module we are looking for """
        if not path.endswith(".py"):
            return False

        f = open(path, "rb")
        data = f.read(16)
        f.close()
        if data.startswith("#/sevabot"):
            return True

        return False

    @fail_safe
    def init(self, skype):
        """
        (Re)load Python code and get access to exported class instance.

        Bound stateful handler to a Skype instance.
        """
        # http://docs.python.org/2/library/imp.html#imp.load_module
        module = imp.load_source(self.name, self.path)
        self.handler = module.sevabot_handler

        self.handler.init(skype)

    @fail_safe
    def shutdown(self):
        """
        Called when we know the stae shutdown will happen.

        E.g. during relaod
        """
        self.handler.shutdown()

    @fail_safe
    def handle(self, msg, status):
        self.handler.handle_message(msg, status)


def load_module(skype, name, path):
    """
    Load a module by name.

    Determine if it's standalone script or stateful.
    """

    if StatefulModule.is_valid(path):
        return StatefulModule(skype, name, path)
    elif UNIXScriptModule.is_valid(path):
        return UNIXScriptModule(name, path)
    else:
        return None


def load_modules(skype):
    """
    Scan all modules folders for executable scripts.

    :param: Skype4Py instance
    """
    for folder in settings.MODULE_PATHS:
        folder = os.path.abspath(folder)
        for f in os.listdir(folder):
            fpath = os.path.join(folder, f)

            # Remove file extension
            body, ext = os.path.splitext(f)

            module = load_module(skype, body, fpath)
            if module:
                logger.info("Discovered module %s: %s" % (body, fpath))
                _modules[body] = module

    if not len(_modules.keys()):
        raise RuntimeError("No modules found in: %s" % settings.MODULE_PATHS)

    return _modules.keys()


def unload_modules():
    """
    """
    for name, mod in _modules.items():
        mod.shutdown()

    _modules.clear()


def get_script_module(name):
    """
    Check if a named module exists.
    """
    mod = _modules.get(name, None)

    if not mod:
        return None

    if isinstance(mod, UNIXScriptModule):
        return mod

    return None


def get_message_handlers():
    """
    Return all stateful module handlers.

    :yield: list of handle(self, msg, status) functions called to every Skype message
    """
    for mod in _modules.values():
        if isinstance(mod, StatefulModule):
            yield mod.handle


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
