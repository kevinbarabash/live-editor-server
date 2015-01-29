__author__ = 'kevin'

import jinja2
import os
from google.appengine.api import users
from google.appengine.api import channel


def authenticate(func):
    def func_wrapper(self):
        user = users.get_current_user()
        if not user:
            self.redirect(users.create_login_url(self.request.uri))
            return
        func(self)
    return func_wrapper


# TODO investigate whether os.getcwd() is really the best choice
jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.getcwd())
)


# these rely on @authenticate and jinja_environment
from editor import Editor
from output import Output
from my_programs import MyPrograms
from all_programs import AllPrograms
from screenshot import Screenshot
from program import CreateProgram
from program import SaveProgram
