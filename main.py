#!/usr/bin/env python

import jinja2
import os
import webapp2
import json
from google.appengine.api import channel
from google.appengine.api import users
from google.appengine.ext import ndb


def user_key(uid):
    return ndb.Key('Account', uid)


class Program(ndb.Model):
    name = ndb.StringProperty()
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
        pid = int(self.request.get("pid"))

        program = Program.get_by_id(pid, parent=user_key(uid))

        # equivalent method:
        # key = ndb.Key('Account', uid, 'Program', pid)
        # program = key.get()

        code = program.code.replace("\n", "\\n").replace("\"", "\\\"")

        if program:
            path = "live-editor/demos/simple/index.html"
            template = jinja_environment.get_template(path)
            template_values = {
                'token': channel.create_channel(uid + "_editor"),
                'id': uid,
                'logout_url': users.create_logout_url(self.request.uri),
                'code': code,
                'pid': pid,
                'title': program.name
            }
            self.response.out.write(template.render(template_values))
        else:
            self.response.out.write("no program with that id")

    @authenticate
    def post(self):
        uid = users.get_current_user().user_id()    # it would be nice to inject if this possible

        # forward the message to the output
        channel.send_message(uid + "_output", self.request.body)


class OutputPage(webapp2.RequestHandler):

    @authenticate
    def get(self):
        uid = users.get_current_user().user_id()

        path = "live-editor/demos/simple/output.html"
        template = jinja_environment.get_template(path)
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


class ProgramList(webapp2.RequestHandler):

    @authenticate
    def get(self):
        uid = users.get_current_user().user_id()
        programs_query = Program.query(ancestor=user_key(uid))
        programs = programs_query.fetch(10)

        for p in programs:
            print p.key.id()

        template = jinja_environment.get_template("html/program_list.html")
        template_values = {
            'programs': programs,
            'logout_url': users.create_logout_url(self.request.uri)
        }
        self.response.out.write(template.render(template_values))


class CreateProgram(webapp2.RequestHandler):

    @authenticate
    def post(self):
        uid = users.get_current_user().user_id()
        name = json.loads(self.request.body)["name"]

        if name:
            program = Program(parent=user_key(uid),
                              name=name,
                              code="rect(100, 100, 100, 100);")
            program.put()

            self.response.set_status(200)


class SaveProgram(webapp2.RequestHandler):

    @authenticate
    def post(self):
        uid = users.get_current_user().user_id()
        body = json.loads(self.request.body)

        print body

        if 'pid' in body:
            pid = int(body['pid'])
            program = Program.get_by_id(pid, parent=user_key(uid))

            if not program:
                self.response.set_status(500)
                self.response.out.write("couldn't retrieve program")

            if 'code' in body:
                program.code = body['code']
                program.put()


jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__))
)

app = webapp2.WSGIApplication([
    ('/editor', EditorPage),
    ('/output', OutputPage),
    ('/programs', ProgramList),
    ('/create', CreateProgram),
    ('/save', SaveProgram)
], debug=True)
