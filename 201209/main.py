#!-*- coding:utf-8 -*-

#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import wsgiref.handlers
import os
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
#from google.appengine.api import mail
from google.appengine.api import users
from google.appengine.ext import db
from google.appengine.api import mail
from django.utils import simplejson

""""""""""""""""""""""""""""""""""""""""
Models
"""""""""""""""""""""""""""""""""""""""

"""
Sessions Model
"""
class Sessions(db.Model):
  name = db.StringProperty(required=True)


"""
Subscribers Model
"""
class Subscribers(db.Model):
  name = db.StringProperty(required=True)
  r0 = db.IntegerProperty(required=False)
  r1 = db.IntegerProperty(required=False)
  r2 = db.IntegerProperty(required=False)
  r3 = db.IntegerProperty(required=False)
  r4 = db.IntegerProperty(required=False)
  r5 = db.IntegerProperty(required=False)




"""
Top page
"""
class MainPage(webapp.RequestHandler):
  def get(self):
    path = os.path.join(os.path.dirname(__file__), 'view/index.html')
    self.response.out.write(template.render(path, {'page':'index'}))

"""
sponsor page
"""
class SponsorPage(webapp.RequestHandler):
  def get(self):
    path = os.path.join(os.path.dirname(__file__), 'view/sponsor.html')
    self.response.out.write(template.render(path, {'page':'sponsor'}))

"""
volunteer page
"""
class VolunteerPage(webapp.RequestHandler):
  def get(self):
    path = os.path.join(os.path.dirname(__file__), 'view/routing.html')
    self.response.out.write(template.render(path, {'filename': 'blocks/volunteer.html', 'page':'volunteer'}))

"""
program page
"""

class ProgramPage(webapp.RequestHandler):
  def get(self):
    program = open(os.path.join(os.path.dirname(__file__), 'datas/program.json')).read()
    progdic = simplejson.loads(program)
    speakers = open(os.path.join(os.path.dirname(__file__), 'datas/speaker.json')).read()
    speadic = simplejson.loads(speakers)

    path = os.path.join(os.path.dirname(__file__), 'view/routing.html')
    self.response.out.write(template.render(path, {'filename': 'blocks/program.html', 'page':'program', 'program': program, 'progdic': progdic, 'speadic': speadic}))

"""
speaker's page
"""

class SpeakerPage(webapp.RequestHandler):
  def get(self):
    program = open(os.path.join(os.path.dirname(__file__), 'datas/program.json')).read()
    progdic = simplejson.loads(program)
    speakers = open(os.path.join(os.path.dirname(__file__), 'datas/speaker.json')).read()
    speadic = simplejson.loads(speakers)
    path = os.path.join(os.path.dirname(__file__), 'view/routing.html')
    self.response.out.write(template.render(path, {'filename': 'blocks/speaker.html', 'page':'speaker', 'program': program, 'progdic': progdic, 'speadic': speadic}))


"""
faq page
"""
class FaqPage(webapp.RequestHandler):
  def get(self):
    path = os.path.join(os.path.dirname(__file__), 'view/routing.html')
    self.response.out.write(template.render(path, {'filename': 'blocks/faq.html', 'page':'faq'}))


"""
registration pages
"""
#class RedirectPage(webapp.RequestHandler):
def loginRequired(self, page):
  str = (u"<a href=\"%s\">login</a>" % users.create_login_url(page))
  path = os.path.join(os.path.dirname(__file__), 'view/login_required.html')
  self.response.out.write(template.render(path, {'page':'login_required', 'mesg':str}))


def topPage(self, alert, params):
  user = users.get_current_user()
  if not user:
    loginRequired(self, "/conference/2012/09/reg_top.html")
    return

  email = user.email()
  path = os.path.join(os.path.dirname(__file__), 'view/reg_top.html')
  self.response.out.write(template.render(path, {'page':'reg_top', 'email':email, 'params': params, 'alert':alert}))

# top
class RegTopPage(webapp.RequestHandler):
  def get(self, alert=[]):
    params = {'name':null, 'confirm':'', 'gender':'', 'generation':'', 'occupation': '', 'how': ''}
    topPage(self, alert, params)

# program
class RegProgramPage(webapp.RequestHandler):
  def post(self):
    user = users.get_current_user()
    if not user:
      loginRequired(self, "/conference/2012/09/reg_program.html")
      return

    # [TODO] First of all, check post parameter and insert to DB
    name = self.request.get('name')
    email = self.request.get('email')
    confirm = self.request.get('confirm')
    gender = self.request.get('gender')
    generation = self.request.get('generation')
    occupation = self.request.get('occupation')
    how = self.request.get('how')

    params = {
      'name': name, 'email': email, 'confirm': confirm, 'gender': gender, 'generation': generation, 'occupation': occupation, 'how': how
    }

    alert=[]

    if not name:
      alert.append("名前が入力されていません")

    if confirm != "yes":
      alert.append("プライバシーポリシーに同意願います")

    if len(alert) != 0:
      topPage(self, alert, params)
      return

    #
    #
    #
    #

    program = open(os.path.join(os.path.dirname(__file__), 'datas/program.json')).read()
    progdic = simplejson.loads(program)
    speakers = open(os.path.join(os.path.dirname(__file__), 'datas/speaker.json')).read()
    speadic = simplejson.loads(speakers)
    email = user.email()

    path = os.path.join(os.path.dirname(__file__), 'view/program.html')
    self.response.out.write(template.render(path, {'email': email,
      'name': name,
      'page':'reg_program',
      'program': program,
      'progdic': progdic,
      'speadic': speadic}))
    """
    email = user.email()
    path = os.path.join(os.path.dirname(__file__), 'view/reg_program.html')
    self.response.out.write(template.render(path, {'page':'reg_program', 'email': email}))
    """
  def get(self):
    user = users.get_current_user()
    if not user:
      loginRequired(self, "/conference/2012/09/reg_program.html")
      return

    email = user.email()
    program = open(os.path.join(os.path.dirname(__file__), 'datas/program.json')).read()
    progdic = simplejson.loads(program)
    speakers = open(os.path.join(os.path.dirname(__file__), 'datas/speaker.json')).read()
    speadic = simplejson.loads(speakers)

    path = os.path.join(os.path.dirname(__file__), 'view/program.html')
    self.response.out.write(template.render(path, {'email': email, 'page':'reg_program', 'program': program, 'progdic': progdic, 'speadic': speadic}))
    """
    path = os.path.join(os.path.dirname(__file__), 'view/reg_program.html')
    self.response.out.write(template.render(path, {'page':'reg_program', 'email': email}))
    """

# confirm
class RegConfirmPage(webapp.RequestHandler):
  def post(self):
    user = users.get_current_user()
    if not user:
      loginRequired(self, "/conference/2012/09/reg_program.html")
      return

    email = user.email()
    slots = [0, 0, 0, 0, 0, 0, 0]
    path = os.path.join(os.path.dirname(__file__), 'view/reg_confirm.html')
    self.response.out.write(template.render(path, {'page':'reg_confirm', 'email': email, 'slots': slots}))
# done
class RegDonePage(webapp.RequestHandler):
  def post(self):
    user = users.get_current_user()
    if not user:
      loginRequired(self, "/conference/2012/09/reg_program.html")
      return

    email = user.email()

    mail.send_mail(sender="kensaku.komatsu@gmail.com",
      to = email,
      subject = "登録ありがとうございます",
      body = """
      HTML5 Conference2012への登録まことにありがとうございます
      お客様の登録状況は以下のとおりです

      hogehoge...
      """)
    path = os.path.join(os.path.dirname(__file__), 'view/reg_done.html')
    self.response.out.write(template.render(path, {'page':'reg_done', 'email': email}))



"""
routing part
"""
def main():
  application = webapp.WSGIApplication([
    ('/conference/2012/09/', MainPage),
    ('/conference/2012/09/index.html', MainPage),
    # ('/conference/2012/09/sponsor.html', SponsorPage),
    ('/conference/2012/09/volunteer.html', VolunteerPage),
    ('/conference/2012/09/program.html', ProgramPage),
    ('/conference/2012/09/speaker.html', SpeakerPage),
    ('/conference/2012/09/faq.html', FaqPage),
    ('/conference/2012/09/reg_top.html', RegTopPage),
    ('/conference/2012/09/reg_program.html', RegProgramPage),
    ('/conference/2012/09/reg_confirm.html', RegConfirmPage),
    ('/conference/2012/09/reg_done.html', RegDonePage)
 ], debug=True)
  wsgiref.handlers.CGIHandler().run(application)

"""
invoke main()
"""
if __name__ == '__main__':
  main()
