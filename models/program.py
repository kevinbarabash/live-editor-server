__author__ = 'kevin'

from google.appengine.ext import ndb


class Program(ndb.Model):
    """
    Model of a user's program.  User's may have multiple programs.
    Program entities where the program's id matches the user's id and there is
    no ancestor are used synchronize initial state between /editor and /output
    """
    creator = ndb.StringProperty()  # user's id
    name = ndb.StringProperty()
    code = ndb.JsonProperty()
    screenshot = ndb.BlobProperty()
