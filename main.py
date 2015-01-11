#!/usr/bin/env python

import jinja2
import os
import webapp2
import json
from google.appengine.api import channel
from google.appengine.api import users
from google.appengine.ext import ndb


class Program(ndb.Model):
    key = ndb.StringProperty()
    code = ndb.JsonProperty()


def authenticate(func):
    def func_wrapper(self):
        user = users.get_current_user()
        if not user:
            self.redirect(users.create_login_url(self.request.uri))
            return
        func(self)
    return func_wrapper


class EditorPage(webapp2.RequestHandler):

    @authenticate
    def get(self):
        uid = users.get_current_user().user_id()

        template = jinja_environment.get_template("demos/simple/index.html")
        template_values = {
            'token': channel.create_channel(uid + "_editor"),
            'id': uid,
            'logout_url': users.create_logout_url(self.request.uri),
        }

        self.response.out.write(template.render(template_values))

    @authenticate
    def post(self):
        uid = users.get_current_user().user_id()    # it would be nice to inject if this possible

        # forward the message
        body = json.loads(self.request.body)
        if 'code' in body:
            program = Program(id=uid, code=body)
            program.put()
            print body
        channel.send_message(uid + "_output", self.request.body)


class OutputPage(webapp2.RequestHandler):

    @authenticate
    def get(self):
        uid = users.get_current_user().user_id()

        template = jinja_environment.get_template("demos/simple/output.html")
        template_values = {
            'token': channel.create_channel(uid + "_output"),
            'id': uid,
            'logout_url': users.create_logout_url(self.request.uri)
        }

        self.response.out.write(template.render(template_values))

    @authenticate
    def post(self):
        body = self.request.body
        uid = users.get_current_user().user_id()    # it would be nice to inject if this possible

        # TODO grab the program from the database based on the program id so it loads faster
        # TODO figure out what to do with other properties such as workersDir, jshintFile, externalsDir, etc.
        # these properties property don't need to be communicated each time
        if body == "connected":
            program = Program.get_by_id(uid)
            if program:
                channel.send_message(uid + "_output", json.dumps(program.code))
        else:
            channel.send_message(uid + "_editor", self.request.body)


class ChannelConnected(webapp2.RequestHandler):

    # this only gets called on the first load in a tab/window
    # if you reload it won't get called so this isn't really that useful
    # because you usually want to get a "connected" message every time you reload the app
    # so that you can do whatever additional initialization is necessary

    def post(self):
        client_id = self.request.get('from')
        print "connected to %s" % client_id


class ChannelDisconnected(webapp2.RequestHandler):

    def post(self):
        client_id = self.request.get('from')
        print "connected from %s" % client_id


jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__))
)

app = webapp2.WSGIApplication([
    ('/editor', EditorPage),
    ('/output', OutputPage),
    ('/_ah/channel/connected/', ChannelConnected),
    ('/_ah/channel/disconnected', ChannelDisconnected)
], debug=True)
