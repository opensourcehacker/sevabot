# -*- coding: utf-8 -*-
"""

    Supported external web service hooks

"""

import json
import logging

from hashlib import md5

from flask.views import View, request

logger = logging.getLogger(__name__)


class SendMessage(View):
    """ A webhook endpoint which sends a message to a Skype chat.

    A generic base class for other webhooks.

    Use HTTP POST parameters

    * msg

    * chat

    Other parameters are for compatibility reasons only and will be removed in the future.

    We validate only shared secret, not message signing.
    """

    methods = ['POST']

    def __init__(self, sevabot, shared_secret):
        self.sevabot = sevabot
        self.shared_secret = shared_secret

    #noinspection PyMethodOverriding
    def dispatch_request(self, *args, **kwargs):

        self.args = args
        self.kwargs = kwargs

        try:
            # BBB: Use only "chat" in the future
            chat_id = self.get_parameter('chat_id') or self.get_parameter('chat')

            if chat_id:
                if not self.validate(kwargs):
                    logger.error("Validation failed")
                    return "Validation failed!", 403, {"Content-type": "text/plain"}
                else:
                    msg = self.compose()

                    if not msg:
                        return "Message payload missing", 500, {"Content-type": "text/plain"}

                    self.sevabot.sendMessage(chat_id, msg)
                    logger.info("Successfully sent message %s" % msg)
                    return "OK"
            else:
                logger.error("Not enough parameters to send message (chat id missing)")
                return "Not enough parameters to send message!", 500, {"Content-type": "text/plain"}
        except Exception as e:
            logger.error(e)
            logger.exception(e)
            return (u"%s" % e).encode("utf-8"), 500, {"Content-type": "text/plain"}

    def get_parameter(self, key):
        """ Return parameter either from request or from url parameters """
        return request.form.get(key) or self.kwargs.get(key)

    def validate(self, kwargs):
        shared_secret = self.get_parameter('shared_secret')
        return shared_secret == self.shared_secret

    def compose(self):
        """
        Parse Skype chat message from the payload.

        .. note ::

            Use msg parameter. Others are provided for backward compatibility.

        """
        return request.form.get('message', '') or request.form.get('msg', '') or request.form.get('data', '')


class SendMessageMD5(SendMessage):
    """
    Send a MD5 signed chat message.

    HTTP POST parameters

    :param chat: Chat id

    :param msg: Message payload

    :param md5: MD5 checksum

    Make sure your client encodes message in UTF-8.
    """
    def validate(self, kwargs):

        # BBB: Use only "chat" in the future
        chat_id = self.get_parameter('chat_id') or self.get_parameter('chat')
        message = self.get_parameter('message') or self.get_parameter('msg')
        md5_value = self.get_parameter('md5')

        chat_encoded = chat_id.encode("utf-8")
        msg_encoded = message.encode("utf-8")

        md5_check = md5(chat_encoded + msg_encoded + self.shared_secret).hexdigest()

        return md5_check == md5_value


class SendMessageUnsigned(SendMessage):
    """
    HTTP endpoint to  send non-verified message to a chat.

    Takes both *chat_id* and *message* parameters as HTTP POST payload.

    .. warn::

        Allows third party to flood the chat if he/she gets hold of a chat id.

    HTTP POST parameters

    :param chat: Chat id

    :param msg: Message payload

    All other HTTP POST parameters are ignored.

    Make sure your client encodes message in UTF-8.
    """
    def validate(self, kwargs):
        return True


class GitHubPostCommit(SendMessage):
    """
    Handle post-commit hook from Github.

    https://help.github.com/articles/post-receive-hooks/
    """

    def compose(self):

        payload = json.loads(request.form["payload"])

        msg = u"(*) %s fresh commits - %s\n" % (payload["repository"]["name"], payload["repository"]["url"])
        for c in payload["commits"]:
            msg += u"(*) %s: %s\n%s\n" % (c["author"]["name"], c["message"], c["url"])

        return msg
		
class GitHubPullRequest(SendMessage):
    """
    Handle post-commit hook from Github.

    https://help.github.com/articles/post-receive-hooks/
    """

    def compose(self):

        payload = json.loads(request.form["payload"])
        
        if payload["action"] == "opened":
            msg = u"(*) %s new pull request %s from %s - %s\n" % (payload["repository"]["name"], payload["number"], payload["pull_request"]["user"]["login"], payload["pull_request"]["html_url"])
        elif payload["action"] == "closed":
            msg = u"(y) %s pull request %s merged by %s - %s\n" % (payload["repository"]["name"], payload["number"], payload["pull_request"]["merged_by"]["login"], payload["pull_request"]["html_url"])
        else:
            msg = u""
        return msg

class JenkinsNotifier(SendMessage):

    """
    Handle requests from Jenkins notifier plugin

    https://wiki.jenkins-ci.org/display/JENKINS/Notification+Plugin
    """

    def compose(self):
        msg = None
        payload = request.json

        if payload is None:
            logger.error("Jenkins did not post a valid HTTP POST payload. Check the logs for further info.")
            return "Jenkins bad notification: Could not read HTTP POST data"
        # Filter out completed status, lots of unneeded noise
        if payload['build']['phase'] != 'COMPLETED':
            if payload['build']['status'] == 'SUCCESS':
                msg = u'Project: %s build #%d %s Status: %s - (sun) - %s\n' % (payload['name'], payload['build']['number'], payload['build']['phase'], payload['build']['status'], payload['build']['full_url'])
            elif payload['build']['status'] == 'FAILURE':
                msg = u'Project: %s build #%d %s Status: %s - (rain) - %s\n' % (payload['name'], payload['build']['number'], payload['build']['phase'], payload['build']['status'], payload['build']['full_url'])
            else:
                msg = u'Project: %s build #%d %s Status: %s - - %s\n' % (payload['name'], payload['build']['number'], payload['build']['phase'], payload['build']['status'], payload['build']['full_url'])

        return msg


class TeamcityWebHook(SendMessage):

    def compose(self):
        payload = json.loads(request.data)
        build = payload.get('build')

        message = '%s\n%s' % (build.get('message'), build.get('buildStatusUrl'))

        return message


def configure(sevabot, settings, server):
    """
    Install Flask webhook routing
    """

       # this url rules for sending message. Parameters can be in url or in request
    server.add_url_rule('/message/', view_func=SendMessage.as_view(str('send_message'), sevabot=sevabot, shared_secret=settings.SHARED_SECRET))

    server.add_url_rule('/message_unsigned/', view_func=SendMessageUnsigned.as_view(str('send_message_unsigned'), sevabot=sevabot, shared_secret=settings.SHARED_SECRET))

    server.add_url_rule('/message/<string:chat_id>/', view_func=SendMessage.as_view(str('send_message_1'), sevabot=sevabot, shared_secret=settings.SHARED_SECRET))

    server.add_url_rule('/message/<string:chat_id>/<string:shared_secret>/', view_func=SendMessage.as_view(str('send_message_2'), sevabot=sevabot, shared_secret=settings.SHARED_SECRET))

    # XXX: Remove
    server.add_url_rule('/zapier/<string:chat_id>/<string:shared_secret>/', view_func=SendMessage.as_view(str('send_message_3'), sevabot=sevabot, shared_secret=settings.SHARED_SECRET))

    # rule for sending md5 signed message
    server.add_url_rule('/msg/', view_func=SendMessageMD5.as_view(str('send_message_md5'), sevabot=sevabot, shared_secret=settings.SHARED_SECRET))

    # rule for notifying on github commits
    server.add_url_rule('/github-post-commit/<string:chat_id>/<string:shared_secret>/', view_func=GitHubPostCommit.as_view(str('send_message_github_1'), sevabot=sevabot, shared_secret=settings.SHARED_SECRET))

    # rule for notifying on github pull requests
    server.add_url_rule('/github-pull-request/<string:chat_id>/<string:shared_secret>/', view_func=GitHubPullRequest.as_view(str('send_message_github_2'), sevabot=sevabot, shared_secret=settings.SHARED_SECRET))

    server.add_url_rule('/jenkins-notifier/<string:chat_id>/<string:shared_secret>/', view_func=JenkinsNotifier.as_view(str('send_message_jenkins'), sevabot=sevabot, shared_secret=settings.SHARED_SECRET))

    server.add_url_rule('/teamcity/<string:chat_id>/<string:shared_secret>/', view_func=TeamcityWebHook.as_view(str('send_message_teamcity'), sevabot=sevabot, shared_secret=settings.SHARED_SECRET))

