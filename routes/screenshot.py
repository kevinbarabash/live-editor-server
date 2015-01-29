__author__ = 'kevin'

import webapp2
import binascii
import json
from urlparse import urlparse

from models import *
from routes import *


class Screenshot(webapp2.RequestHandler):

    @authenticate
    def get(self):
        path = urlparse(self.request.url).path
        parts = path[1:].split("/")

        if len(parts) < 2:
            self.response.set_status(500)
            self.response.out.write("program id not specified in URL")

        pid = int(parts[1])

        program = Program.get_by_id(pid)

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

        status = 'failure'

        # TODO proper logging
        if 'pid' in body:
            print 'pid = %s' % body['pid']
        else:
            self.response.set_status(500)
            self.response.out.write("pid wasn't sent as part of request")

        # TODO proper logging
        if 'data' in body:
            print 'len(data) = %d' % len(body['data'])
        else:
            self.response.set_status(500)
            self.response.out.write("data wasn't sent as part of request")

        pid = int(body['pid'])
        data = body['data']
        program = Program.get_by_id(pid)

        if not program:
            self.response.set_status(500)
            self.response.out.write("couldn't retrieve program")
        else:
            program.screenshot = data.encode('ascii')
            program.put()

            # TODO proper logging
            print "sucessfully saved an image for program: %d" % pid

            status = 'success'

        msg = {'screenshot': status}
        channel.send_message(uid + "_editor", json.dumps(msg))
