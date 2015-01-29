__author__ = 'kevin'

import webapp2

from models import *
from routes import *


class AllPrograms(webapp2.RequestHandler):

    @authenticate
    def get(self):
        query = Program.query(Program.creator != None)
        programs = query.fetch(10)

        template = jinja_environment.get_template("html/all_programs.html")
        template_values = {
            'programs': programs
        }
        self.response.out.write(template.render(template_values))
