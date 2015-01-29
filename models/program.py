__author__ = 'kevin'

from google.appengine.ext import ndb


def user_key(uid):
    """
    Creates an instance of Key with type 'Account'.
    Currently 'Account' is an opaque type with no fields, but this may change
    in the future.
    :param uid: integer
    :return: ndb.Key
    """
    return ndb.Key('Account', uid)


class Program(ndb.Model):
    """
    Model of a user's program.  User's may have multiple programs.
    Program entities where the program's id matches the user's id and there is
    no ancestor are used synchronize initial state between /editor and /output
    """
    name = ndb.StringProperty()
    code = ndb.JsonProperty()
    screenshot = ndb.BlobProperty()
