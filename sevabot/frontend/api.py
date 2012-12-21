#!/usr/bin/env python
# coding=utf-8

import json
import logging
from hashlib import md5

from flask.views import View, request

logger = logging.getLogger(__name__)

class SendMessage(View):

    methods = ['POST']

    def __init__(self, sevabot, shared_secret):
        self.sevabot = sevabot
        self.shared_secret = shared_secret

    #noinspection PyMethodOverriding
    def dispatch_request(self, *args, **kwargs):

        self.args = args
        self.kwargs = kwargs

        try:
            chat_id = self.get_parameter('chat_id')

            if chat_id:
                if not self.validate(kwargs):
                    return "Validation failed!", 403, {"Content-type": "text/plain"}
                else:
                    self.sevabot.sendMsg(chat_id, self.compose())
                    return "OK"
            else:
                return "Not enough parameters to send message!", 500, {"Content-type": "text/plain"}
        except Exception as e:
            logger.error(e)
            logger.exception(e)
            return unicode(e)

    def get_parameter(self, key):
        """ Return parameter either from request or from url parameters """
        return request.form.get(key) or self.kwargs.get(key)

    def validate(self, kwargs):
        shared_secret = self.get_parameter('shared_secret')
        return shared_secret == self.shared_secret

    def compose(self):
        return request.form.get('message', '')


class SendMessageMD5(SendMessage):
    def validate(self, kwargs):

        chat_id = self.get_parameter('chat_id')
        message = self.get_parameter('message')
        md5_value = self.get_parameter('md5')

        chat_encoded = chat_id.encode("utf-8")
        msg_encoded = message.encode("utf-8")

        md5_check = md5(chat_encoded + msg_encoded + self.shared_secret).hexdigest()

        return md5_check == md5_value


class GitHubPostCommit(SendMessage):
    """
    Handle post-commit hook from Github.

    https://help.github.com/articles/post-receive-hooks/
    """

    def compose(self):

        payload = json.loads(request.form["payload"])

        msg = u"★ %s fresh commits 〜 %s\n" % (payload["repository"]["name"], payload["repository"]["url"])
        for c in payload["commits"]:
            msg += u"★ %s: %s\n%s\n" % (c["author"]["name"], c["message"], c["url"])

        return msg

class JenkinsNotifier(SendMessage):
    """
    Handle requests from Jenkins notifier plugin

    https://wiki.jenkins-ci.org/display/JENKINS/Notification+Plugin
    """

    def compose(self):

        payload = json.loads(request.form.keys()[0])

        # Filter out completed status, lots of unneeded noise
        if ( payload["build"]["phase"]  != 'COMPLETED' ):
            if ( payload["build"]["status"]  == 'SUCCESS' ):
                msg = u"Project: %s build #%d %s Status: %s - (sun) - %s\n" % (payload["name"], payload["build"]["number"],payload["build"]["phase"],payload["build"]["status"],payload["build"]["full_url"])
            elif ( payload["build"]["status"]  == 'FAILURE' ):
                msg = u"Project: %s build #%d %s Status: %s - (rain) - %s\n" % (payload["name"], payload["build"]["number"],payload["build"]["phase"],payload["build"]["status"],payload["build"]["full_url"])
            else:
                msg = u"Project: %s build #%d %s Status: %s - - %s\n" % (payload["name"], payload["build"]["number"],payload["build"]["phase"],payload["build"]["status"],payload["build"]["full_url"])

        return msg

class TeamcityWebHook(SendMessage):

    def compose(self):
        payload = json.loads(request.data)
        build = payload.get('build')

        message = '%s\n%s' % (build.get('message'), build.get('buildStatusUrl'))

        return message

if __name__ == '__main__':
    pass
