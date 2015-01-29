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
        o = urlparse(self.request.url)
        self.response.out.write("echo: " + o.path)


# TODO migrate to Cloud Endpoints
app = webapp2.WSGIApplication([
    ('/editor', Editor),
    ('/output', Output),
    ('/my_programs', MyPrograms),
    ('/create', CreateProgram),
    ('/save', SaveProgram),
    ('/screenshot', Screenshot),
    ('/all_programs', AllPrograms),
    ('/', Redirect),
    ('/echo/.*', Echo)
], debug=True)
