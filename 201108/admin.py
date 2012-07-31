#!-*- coding:utf-8 -*-

import wsgiref.handlers
import os
from attend import Attend
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.api import users

class Check(webapp.RequestHandler):
  def get(self):
    greeting = "U"

    self.response.out.write("Hello, %s!!" % greeting)

"""
Mainのルーティング部
"""
def main():
  application = webapp.WSGIApplication([
      ('/admin/', Check),
    ], debug=True)
  wsgiref.handlers.CGIHandler().run(application)

"""
main()のinvoke
"""
if __name__ == '__main__':
  main()
