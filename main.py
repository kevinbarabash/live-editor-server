#!/usr/bin/env python

import webapp2

from routes import *


class Redirect(webapp2.RequestHandler):

    @authenticate
    def get(self):
        self.redirect('/my_programs')


# TODO migrate to Cloud Endpoints
app = webapp2.WSGIApplication([
    ('/editor', Editor),
    ('/output', Output),
    ('/my_programs', MyPrograms),
    ('/create', CreateProgram),
    ('/save', SaveProgram),
    ('/screenshot', Screenshot),
    ('/all_programs', AllPrograms),
    ('/', Redirect)
], debug=True)
