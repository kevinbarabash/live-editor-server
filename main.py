#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import jinja2
import os
import webapp2
from google.appengine.api import channel
from google.appengine.api import users
from google.appengine.ext import ndb


class Program(ndb.Model):
    key = ndb.StringProperty()
    code = ndb.JsonProperty()


class MainPage(webapp2.RequestHandler):

    def get(self):
        user = users.get_current_user()
        if not user:
            self.redirect(users.create_login_url(self.request.uri))
            return

        # TODO: use the program id as the key
        uid = user.user_id()
        role = self.request.get('role')

        token = channel.create_channel(uid + "_" + role)

        if role == "editor":
            # TODO: create an entry right away because we're getting the code from the server to generate this page
            code = 'console.log("hello, world!");'
            prog = Program(id=uid, code=code)
            prog.put()
            template = jinja_environment.get_template('editor.html')
            pass
        elif role == "output":
            prog = Program.get_by_id(uid)
            code = prog.code
            template = jinja_environment.get_template('output.html')
            pass
        else:
            raise Exception("role not defined")

        template_values = {
            'token': token,
            'id': uid,
            'code': code,
            'role': role
        }

        self.response.out.write(template.render(template_values))


class UpdatePage(webapp2.RequestHandler):

    def post(self):
        user = users.get_current_user()
        uid = user.user_id()
        role = self.request.get('role')
        message = self.request.get('message')

        print "uid = %s, role = %s, message = %s" % (uid, role, message)
        if role == "editor":
            channel.send_message(uid + "_output", message)
        elif role == "output":
            channel.send_message(uid + "_editor", message)
        pass


jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__))
)

app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/update', UpdatePage)
], debug=True)



# class MainHandler(webapp2.RequestHandler):
#     def get(self):
#         self.response.write('Hello world!')
#
# app = webapp2.WSGIApplication([
#     ('/', MainHandler)
# ], debug=True)
