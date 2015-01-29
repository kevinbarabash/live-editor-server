#!/usr/bin/env python

import webapp2
from urlparse import urlparse

from routes import *


class Redirect(webapp2.RequestHandler):

    @authenticate
    def get(self):
        self.redirect('/my_programs')


class Echo(webapp2.RequestHandler):

    @authenticate
    def get(self):
        path = urlparse(self.request.url).path
        parts = path[1:].split("/")
        if len(parts) == 2:
            eid = parts[1]
            self.response.out.write("echo: " + eid)



# TODO migrate to Cloud Endpoints
app = webapp2.WSGIApplication([
    ('/editor/.*', Editor),
    ('/editor', Editor),
    ('/output', Output),
    ('/my_programs', MyPrograms),
    ('/create', CreateProgram),
    ('/save', SaveProgram),
    ('/screenshot/.*', Screenshot),
    ('/screenshot', Screenshot),
    ('/all_programs', AllPrograms),
    ('/', Redirect),
    ('/echo/.*', Echo)
], debug=True)
