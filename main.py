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


# TODO: consider using factory pattern since EditorPage and OutputPage so similar
class EditorPage(webapp2.RequestHandler):

    @authenticate
    def get(self):
        uid = users.get_current_user().user_id()

        # TODO: grab code from the DataStore
        # TODO: have some canned programs that already in the DataStore
        code = 'console.log("hello, world!");'
        prog = Program(id=uid, code=code)
        prog.put()

        template = jinja_environment.get_template('editor.html')
        template_values = {
            'token': channel.create_channel(uid + "_editor"),
            'id': uid,
            'code': code,
            'logout_url': users.create_logout_url(self.request.uri)
        }

        self.response.out.write(template.render(template_values))

    @authenticate
    def post(self):
        uid = users.get_current_user().user_id()    # it would be nice to inject if this possible
        body = json.loads(self.request.body)
        print body

        data = {"message": body["message"], "time": body["time"]}
        channel.send_message(uid + "_output", json.dumps(data))


class OutputPage(webapp2.RequestHandler):

    @authenticate
    def get(self):
        uid = users.get_current_user().user_id()

        prog = Program.get_by_id(uid)
        code = prog.code

        template = jinja_environment.get_template('output.html')
        template_values = {
            'token': channel.create_channel(uid + "_output"),
            'id': uid,
            'code': code,
            'logout_url': users.create_logout_url(self.request.uri)
        }

        self.response.out.write(template.render(template_values))

    @authenticate
    def post(self):
        uid = users.get_current_user().user_id()    # it would be nice to inject if this possible
        body = json.loads(self.request.body)
        print body

        data = {"message": body["message"], "time": body["time"]}
        channel.send_message(uid + "_editor", json.dumps(data))


jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__))
)

app = webapp2.WSGIApplication([
    ('/editor', EditorPage),
    ('/output', OutputPage)
], debug=True)
