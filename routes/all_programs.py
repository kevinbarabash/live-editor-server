__author__ = 'kevin'

import webapp2

from models import *
from routes import *


class AllPrograms(webapp2.RequestHandler):

    @authenticate
    def get(self):
        query = Program.query()
        programs = query.fetch(10)

        filtered_programs = [p for p in programs if p.key.parent() is not None]

        template = jinja_environment.get_template("html/all_programs.html")
        template_values = {
            'programs': filtered_programs
        }
        self.response.out.write(template.render(template_values))
