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
            program = Program(creator=uid,
                              name=name,
                              code="rect(100, 100, 100, 100);")
            program.put()

            self.response.set_status(200)
            self.response.out.write(program.key.id())


class SaveProgram(webapp2.RequestHandler):

    @authenticate
    def post(self):
        body = json.loads(self.request.body)

        if 'pid' in body:
            pid = int(body['pid'])
            uid = users.get_current_user().user_id()
            program = Program.get_by_id(pid)

            if program.creator != uid:
                self.response.set_status(403)
                self.response.out.write("can only modify your programs")

            if not program:
                self.response.set_status(404)
                self.response.out.write("program not found")

            if 'code' in body:
                program.code = body['code']
                program.put()
