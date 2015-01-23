#!/usr/bin/env python

import jinja2
import os
import webapp2
import json
import binascii
from google.appengine.api import channel
from google.appengine.api import users
from google.appengine.ext import ndb


def user_key(uid):
    return ndb.Key('Account', uid)


class Program(ndb.Model):
    name = ndb.StringProperty()
    code = ndb.JsonProperty()
    screenshot = ndb.BlobProperty()


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
        user = users.get_current_user()
        uid = user.user_id()
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
                'title': program.name,
                'nickname': user.nickname()
            }
            self.response.out.write(template.render(template_values))
        else:
            self.response.out.write("no program with that id")

    @authenticate
    def post(self):
        uid = users.get_current_user().user_id()    # it would be nice to inject if this possible

        # Save a copy of the program with the id of the user
        # this program doesn't show up in the list of user's program
        # it's used to store the current state of whatever the user
        # is editing so that when they reload /output on a different
        # browser window they'll be able to view the last edit state
        # without having to wait for the editor to push changes.
        # See OutputPage:post in particular dealing with "connected" messages
        body = json.loads(self.request.body)
        if 'code' in body:
            program = Program(id=uid, code=body)
            program.put()

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
        user = users.get_current_user()
        uid = user.user_id()
        programs_query = Program.query(ancestor=user_key(uid))
        programs = programs_query.fetch(10)
        # TODO: add a show-more button if there's more

        template = jinja_environment.get_template("html/program_list.html")
        template_values = {
            'programs': programs,
            'logout_url': users.create_logout_url(self.request.uri),
            'nickname': user.nickname()
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
            self.response.out.write(program.key.id())


class SaveProgram(webapp2.RequestHandler):

    @authenticate
    def post(self):
        uid = users.get_current_user().user_id()
        body = json.loads(self.request.body)

        if 'pid' in body:
            pid = int(body['pid'])
            program = Program.get_by_id(pid, parent=user_key(uid))

            if not program:
                self.response.set_status(500)
                self.response.out.write("couldn't retrieve program")

            if 'code' in body:
                program.code = body['code']
                program.put()


class Screenshot(webapp2.RequestHandler):

    @authenticate
    def get(self):
        uid = self.request.get("uid")
        if uid is "":
            uid = users.get_current_user().user_id()
        pid = int(self.request.get("pid"))

        program = Program.get_by_id(pid, parent=user_key(uid))

        if program:
            if program.screenshot:
                data_uri = program.screenshot
                comma_pos = data_uri.find(",")
                _, head = data_uri[:comma_pos].split(":")
                parts = head.split(";")
                mime = parts[0]
                data = program.screenshot[comma_pos + 1:]
                self.response.headers['Content-Type'] = mime
                self.response.out.write(binascii.a2b_base64(data))
            else:
                self.redirect("/images/blank-200x200.png")

    @authenticate
    def post(self):
        uid = users.get_current_user().user_id()
        body = json.loads(self.request.body)

        if 'pid' in body:
            print 'pid = %s' % body['pid']
        else:
            self.response.set_status(500)
            self.response.out.write("pid wasn't sent as part of request")

        if 'data' in body:
            print 'len(data) = %d' % len(body['data'])
        else:
            self.response.set_status(500)
            self.response.out.write("data wasn't sent as part of request")

        pid = int(body['pid'])
        data = body['data']
        program = Program.get_by_id(pid, parent=user_key(uid))

        if not program:
            self.response.set_status(500)
            self.response.out.write("couldn't retrieve program")
        else:
            program.screenshot = data.encode('ascii')
            program.put()
            print "sucessfully saved an image for program: %d" % pid


class AllPrograms(webapp2.RequestHandler):

    @authenticate
    def get(self):
        query = Program.query()
        programs = query.fetch(10)

        filtered_programs = [p for p in programs if p.key.parent() is not None]

        template = jinja_environment.get_template("html/all_programs.html")
        template_values = {
            'programs': filtered_programs
        }
        self.response.out.write(template.render(template_values))


jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__))
)

app = webapp2.WSGIApplication([
    ('/editor', EditorPage),
    ('/output', OutputPage),
    ('/my_programs', ProgramList),
    ('/create', CreateProgram),
    ('/save', SaveProgram),
    ('/screenshot', Screenshot),
    ('/all_programs', AllPrograms)
], debug=True)
