import cgi

from google.appengine.api import users
from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app

from google.appengine.ext.db import djangoforms
class Attend(db.Model):
  name = db.StringProperty(required=True)
  email = db.EmailProperty(required=True)
  belonging = db.StringProperty(required=True)
  category = db.StringListProperty(required=True)
  sex = db.StringProperty(required=True)
  track = db.StringListProperty(required=True)
  handson = db.StringProperty(required=True)
  lt = db.StringProperty(required=True)
  comment = db.StringProperty(required=False)


class AttendForm(djangoforms.ModelForm):
  class Meta:
    model = Attend