__author__ = 'kevin'

import webapp2
import json
from urlparse import urlparse

from models import *
from routes import *


class Editor(webapp2.RequestHandler):

    @authenticate
    def get(self):
        user = users.get_current_user()
        uid = user.user_id()
        path = urlparse(self.request.url).path
        parts = path[1:].split("/")

        if len(parts) < 2:
            self.response.set_status(500)
            self.response.out.write("program id not specified in URL")

        pid = int(parts[1])
        program = Program.get_by_id(pid) #, parent=user_key(uid))

        # equivalent method:
        # key = ndb.Key('Account', uid, 'Program', pid)
        # program = key.get()

        code = program.code.replace("\n", "\\n").replace("\"", "\\\"")

        if uid == program.creator:
            allowSave = "true"
            allowScreenshot = "true"
        else:
            allowSave = "false"
            allowScreenshot = "false"

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
                'creator': program.creator,
                'nickname': user.nickname(),
                'allowSave': allowSave,
                'allowScreenshot': allowScreenshot
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
