__author__ = 'kevin'

import webapp2
import json

from models import *
from routes import *


class Output(webapp2.RequestHandler):

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
        uid = users.get_current_user().user_id()
        # it would be nice to inject if this possible

        # TODO grab the program from the database based on the program id so it loads faster
        # TODO figure out what to do with other properties such as workersDir, jshintFile, externalsDir, etc.
        # these properties property don't need to be communicated each time
        if body == "connected":
            program = Program.get_by_id(uid)
            if program:
                channel.send_message(uid + "_output", json.dumps(program.code))
        else:
            channel.send_message(uid + "_editor", self.request.body)
