#!/sevabot
"""

    Simple group chat task manager.

    This also serves as an example how to write stateful handlers.

"""

from __future__ import unicode_literals

from datetime import datetime
import os
import logging
import pickle
from collections import OrderedDict

from sevabot.bot.stateful import StatefulSkypeHandler
from sevabot.utils import ensure_unicode, get_chat_id

logger = logging.getLogger("Tasks")

logger.debug("Tasks module level load import")

MAX_TASK_DURATION = 24*60*60

HELP_TEXT = """!tasks is a noteboard where virtual team members can share info which tasks they are currently working on.

Commands
------------------------------

!tasks: This help text

Start task: You start working on a task. When you started is recorded. Example:

    start task I am now working on new Sevabot module interface

Stop task: Stop working on the current task. Example:

    stop task

List tasks: List all tasks an people working on them. Example:

    list tasks

Task lists are chat specific and the list is secure to the members of the chat.
All commands are case-insensitive.
"""


class TasksHandler(StatefulSkypeHandler):
    """
    Skype message handler class for the task manager.
    """

    def __init__(self):
        """Use `init` method to initialize a handler.
        """
        logger.debug("Tasks constructed")

    def init(self, skype):
        """
        Set-up our state. This is called

        :param skype: Handle to Skype4Py instance
        """
        logger.debug("Tasks init")
        self.skype = skype
        self.status_file = os.path.join(os.path.dirname(__file__), "sevabot-tasks.tmp")
        self.status = Status.read(self.status_file)

        self.commands = {
            "!tasks": self.help,
            "start task": self.start_task,
            "list tasks": self.list_tasks,
            "stop task": self.stop_task,
        }

    def handle_message(self, msg, status):
        """Override this method to customize a handler.
        """

        # Skype API may give different encodings
        # on different platforms
        body = ensure_unicode(msg.Body)

        logger.debug("Tasks handler got: %s" % body)

        words = body.split(" ")
        lower = body.lower()

        if len(words) == 0:
            return False

        # Parse argument for two part command names
        if len(words) >= 2:
            desc = " ".join(words[2:])
        else:
            desc = None

        chat_id = get_chat_id(msg.Chat)

        for name, cmd in self.commands.items():
            if lower.startswith(name):
                cmd(msg, status, desc, chat_id)
                return True

        return False

    def shutdown():
        """ Called when the module is reloaded.
        """
        logger.debug("Tasks handler shutdown")

    def save(self):
        """
        Persistent our state.
        """
        Status.write(self.status_file, self.status)

    def help(self, msg, status, desc, chat_id):
        """
        """

        # Make sure we don't trigger ourselves with the help text
        if not desc:
            msg.Chat.SendMessage(HELP_TEXT)

    def start_task(self, msg, status, desc, chat_id):
        """
        """

        if desc.strip() == "":
            msg.Chat.SendMessage("Please give task description also")
            return

        tasks = self.status.get_tasks(chat_id)
        existing_job = tasks.get(msg.Sender.Handle, None)
        if existing_job:
            msg.Chat.SendMessage("Stopped existing task %s" % existing_job.desc)

        job = Job(msg.Sender.FullName, datetime.now(), desc)
        tasks = self.status.get_tasks(chat_id)
        tasks[msg.Sender.Handle] = job
        self.save()
        msg.Chat.SendMessage("%s started working on %s." % (job.real_name, job.desc))

    def list_tasks(self, msg, status, desc, chat_id):
        """
        """

        jobs = self.status.get_tasks(chat_id).values()

        if len(jobs) == 0:
            msg.Chat.SendMessage("No active tasks for anybody")

        for job in jobs:
            msg.Chat.SendMessage("%s started working on %s, %s" % (job.real_name, job.desc, pretty_time_delta(job.started)))

    def stop_task(self, msg, status, desc, chat_id):
        """
        """
        tasks = self.status.get_tasks(chat_id)
        if msg.Sender.Handle in tasks:
            job = tasks[msg.Sender.Handle]
            del tasks[msg.Sender.Handle]
            msg.Chat.SendMessage("%s finished" % job.desc)
        else:
            msg.Chat.SendMessage("%s had no active task" % msg.Sender.FullName)

        self.save()


class Status:
    """
    Stored pickled state of the tasks.

    Use Python pickling serialization for making status info persistent.
    """

    def __init__(self):
        # Chat id -> OrderedDict() of jobs mappings
        self.chats = dict()

    @classmethod
    def read(cls, path):
        """
        Read status file.

        Return fresh status if file does not exist.
        """

        if not os.path.exists(path):
            # Status file do not exist, get default status
            return Status()

        f = open(path, "rb")

        try:
            return pickle.load(f)
        finally:
            f.close()

    @classmethod
    def write(cls, path, status):
        """
        Write status file
        """
        f = open(path, "wb")
        pickle.dump(status, f)
        f.close()

    def get_tasks(self, chat_id):
        """
        Get Chats of a particular job.
        """
        if not chat_id in self.chats:
            # Skype username -> Task instance mappings
            self.chats[chat_id] = OrderedDict()

        return self.chats[chat_id]


class Job:
    """
    Tracks who is doing what
    """

    def __init__(self, real_name, started, desc):
        """
        :param started: datetime when the job was started
        """
        self.started = started
        self.desc = desc
        self.real_name = real_name


# The following has been
# ripped off from https://github.com/imtapps/django-pretty-times/blob/master/pretty_times/pretty.py

_ = lambda x: x


def pretty_time_delta(time):

    now = datetime.now(time.tzinfo)

    if time > now:
        past = False
        diff = time - now
    else:
        past = True
        diff = now - time

    days = diff.days

    if days is 0:
        return get_small_increments(diff.seconds, past)
    else:
        return get_large_increments(days, past)


def get_small_increments(seconds, past):
    if seconds < 10:
        result = _('just now')
    elif seconds < 60:
        result = _pretty_format(seconds, 1, _('seconds'), past)
    elif seconds < 120:
        result = past and _('a minute ago') or _('in a minute')
    elif seconds < 3600:
        result = _pretty_format(seconds, 60, _('minutes'), past)
    elif seconds < 7200:
        result = past and _('an hour ago') or _('in an hour')
    else:
        result = _pretty_format(seconds, 3600, _('hours'), past)
    return result


def get_large_increments(days, past):
    if days == 1:
        result = past and _('yesterday') or _('tomorrow')
    elif days < 7:
        result = _pretty_format(days, 1, _('days'), past)
    elif days < 14:
        result = past and _('last week') or _('next week')
    elif days < 31:
        result = _pretty_format(days, 7, _('weeks'), past)
    elif days < 61:
        result = past and _('last month') or _('next month')
    elif days < 365:
        result = _pretty_format(days, 30, _('months'), past)
    elif days < 730:
        result = past and _('last year') or _('next year')
    else:
        result = _pretty_format(days, 365, _('years'), past)
    return result


def _pretty_format(diff_amount, units, text, past):
    pretty_time = (diff_amount + units / 2) / units

    if past:
        base = "%(amount)d %(quantity)s ago"
    else:
        base = "%(amount)d %(quantity)s"

    return base % dict(amount=pretty_time, quantity=text)


# Export the instance to Sevabot
sevabot_handler = TasksHandler()

__all__ = ["sevabot_handler"]
