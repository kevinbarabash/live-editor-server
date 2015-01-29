__author__ = 'kevin'

import webapp2
import json

from models import *
from routes import *


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
