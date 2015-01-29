__author__ = 'kevin'

import webapp2

from models import *
from routes import *


class MyPrograms(webapp2.RequestHandler):

    @authenticate
    def get(self):
        user = users.get_current_user()
        uid = user.user_id()
        programs_query = Program.query(ancestor=user_key(uid))
        programs = programs_query.fetch(10)
        # TODO: add a show-more button if there's more

        template = jinja_environment.get_template("html/program_list.html")
        template_values = {
            'programs': programs,
            'logout_url': users.create_logout_url(self.request.uri),
            'nickname': user.nickname()
        }
        self.response.out.write(template.render(template_values))
