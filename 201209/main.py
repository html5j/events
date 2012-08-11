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
class Session(db.Model):
  session_id = db.IntegerProperty(required=True)
  max_ = db.IntegerProperty(required=True)
  curr_ = db.IntegerProperty(required=True, default=0)
  status = db.StringProperty(required=True, default="ok")


"""
Subscribers Model
"""
class Users(db.Model):
  name = db.StringProperty(required=True)
  email = db.StringProperty(required=True)
  gender = db.StringProperty(required=False)
  generation = db.StringProperty(required=False)
  occupation = db.StringProperty(required=False)
  how = db.StringProperty(required=False)
  created = db.DateTimeProperty(auto_now_add=True)
  slot_0 = db.StringProperty(required=False)
  slot_2 = db.StringProperty(required=False)
  slot_4 = db.StringProperty(required=False)
  slot_6 = db.StringProperty(required=False)
  slot_8 = db.StringProperty(required=False)
  slot_10 = db.StringProperty(required=False)
  slot_12 = db.StringProperty(required=False)
  canceld = db.BooleanProperty(required=True, default=False)


def getCurrentNum():
  q =  Users.all()
  q.filter('canceld =', False)

  return len(q.fetch(1000))

def canSubscribe():
  max_ = 1000
  curr = getCurrentNum()

  if curr > max_:
    return False
  else:
    return True


"""
Top page
"""
class MainPage(webapp.RequestHandler):
  def get(self):
    path = os.path.join(os.path.dirname(__file__), 'view/index.html')
    self.response.out.write(template.render(path, {'page':'index', 'can_subscribe': canSubscribe()}))

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
lt page
"""
class LtPage(webapp.RequestHandler):
  def get(self):
    path = os.path.join(os.path.dirname(__file__), 'view/routing.html')
    self.response.out.write(template.render(path, {'filename': 'blocks/lt.html', 'page':'lt'}))

"""
writer page
"""
class WriterPage(webapp.RequestHandler):
  def get(self):
    path = os.path.join(os.path.dirname(__file__), 'view/routing.html')
    self.response.out.write(template.render(path, {'filename': 'blocks/writer.html', 'page':'writer'}))

"""
program page
"""

def getSessions():
  q = Session.all()
  return q.fetch(100)

class ProgramPage(webapp.RequestHandler):
  def get(self):
    program = open(os.path.join(os.path.dirname(__file__), 'datas/program.json')).read()
    progdic = simplejson.loads(program)
    speakers = open(os.path.join(os.path.dirname(__file__), 'datas/speaker.json')).read()
    speadic = simplejson.loads(speakers)



    path = os.path.join(os.path.dirname(__file__), 'view/routing.html')
    self.response.out.write(template.render(path, {'filename': 'blocks/program.html', 'sess': getSessions(), 'page':'program', 'program': program, 'progdic': progdic, 'speadic': speadic}))

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

  user_tbl = getUserTbl(user)

  if user_tbl and not user_tbl[0].canceld:
    self.redirect('/conference/2012/09/reg_program.html')
    return

  email = user.email()
  path = os.path.join(os.path.dirname(__file__), 'view/reg_top.html')
  self.response.out.write(template.render(path, {'page':'reg_top', 'email':email, 'params': params, 'alert':alert, 'can_subscribe': canSubscribe()}))

# top
class RegTopPage(webapp.RequestHandler):
  def get(self, alert=[]):
    program = open(os.path.join(os.path.dirname(__file__), 'datas/program.json')).read()
    progdic = simplejson.loads(program)

    for slot in progdic:
      if "sessions" in slot:
        for session in slot.get('sessions'):
          sess = Session.get_by_key_name(str(session['session_id']))
          if sess:
            sess.max_ = session['max']
          else:
            sess = Session(key_name = str(session['session_id']), session_id = session['session_id'], max_ = session['max'])
          sess.put()

    params = {'name':'', 'confirm':'', 'gender':'', 'generation':'', 'occupation': '', 'how': ''}
    topPage(self, alert, params)

def getUserTbl(user):
  email = user.email()

  query = Users.all()
  query.filter('email =', email)
  res = query.fetch(1)

  return res

# program
class RegProgramPage(webapp.RequestHandler):
  def post(self):
    user = users.get_current_user()
    if not user:
      loginRequired(self, "/conference/2012/09/reg_program.html")
      return

    user_tbls = getUserTbl(user)

    #if user_tbls:
    #  self.redirect("/conference/2012/09/program.html")
    #  return

    if not user_tbls or user_tbls[0].canceld:
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

      if not user_tbls:
        user = Users(name = name, email = email)
        user.gender = gender
        user.generation = generation
        user.occupation = occupation
        user.how = how
        user.canceld = False
        user.put()

        user_tbl = user
      else:
        user_tbl = user_tbls[0]
        user_tbl.name = name
        user_tbl.gender = gender
        user_tbl.generation = generation
        user_tbl.occupation = occupation
        user_tbl.how = how
        user_tbl.canceld = False
        user_tbl.put()

    else:
      user_tbl = user_tbls[0]

    #
    #
    #
    #


    program = open(os.path.join(os.path.dirname(__file__), 'datas/program.json')).read()
    progdic = simplejson.loads(program)
    speakers = open(os.path.join(os.path.dirname(__file__), 'datas/speaker.json')).read()
    speadic = simplejson.loads(speakers)


    path = os.path.join(os.path.dirname(__file__), 'view/program.html')
    self.response.out.write(template.render(path, {
      'user_tbl': user_tbl,
      'sess': getSessions(),
      'page':'reg_program',
      'program': program,
      'progdic': progdic,
      'speadic': speadic}))
  def get(self):
    user = users.get_current_user()
    if not user:
      loginRequired(self, "/conference/2012/09/reg_program.html")
      return

    user_tbls = getUserTbl(user)
    # if user_tbls:
    #  self.redirect("/conference/2012/09/program.html")
    #   return

    if not user_tbls:
      self.redirect('/conference/2012/09/reg_top.html')
      return
    user_tbl = user_tbls[0]

    email = user_tbl.email
    name = user_tbl.name
    registered = []
    if user_tbl.slot_0:
      registered.append(int(user_tbl.slot_0))
    if user_tbl.slot_2:
      registered.append(int(user_tbl.slot_2))
    if user_tbl.slot_4:
      registered.append(int(user_tbl.slot_4))
    if user_tbl.slot_6:
      registered.append(int(user_tbl.slot_6))
    if user_tbl.slot_8:
      registered.append(int(user_tbl.slot_8))
    if user_tbl.slot_10:
      registered.append(int(user_tbl.slot_10))
    if user_tbl.slot_12:
      registered.append(int(user_tbl.slot_12))

    program = open(os.path.join(os.path.dirname(__file__), 'datas/program.json')).read()
    progdic = simplejson.loads(program)
    speakers = open(os.path.join(os.path.dirname(__file__), 'datas/speaker.json')).read()
    speadic = simplejson.loads(speakers)

    path = os.path.join(os.path.dirname(__file__), 'view/program.html')
    self.response.out.write(template.render(path, {'user_tbl': user_tbl, 'sess': getSessions(), 'registered': registered, 'page':'reg_program', 'program': program, 'progdic': progdic, 'speadic': speadic}))

# [TODO] duplicat => confirm
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

class CancelDonePage(webapp.RequestHandler):
  def get(self):
    user = users.get_current_user()
    if not user:
      self.redirect('/conference/2012/09/')
      return

    user_tbls = getUserTbl(user)
    if not user_tbls:
      self.redirect('/conference/2012/09/')
      return

    user_tbl = user_tbls[0]
    keys = []
    if user_tbl.slot_0:
      keys.append(str(user_tbl.slot_0))
    if user_tbl.slot_2:
      keys.append(str(user_tbl.slot_2))
    if user_tbl.slot_4:
      keys.append(str(user_tbl.slot_4))
    if user_tbl.slot_6:
      keys.append(str(user_tbl.slot_6))
    if user_tbl.slot_8:
      keys.append(str(user_tbl.slot_8))
    if user_tbl.slot_10:
      keys.append(str(user_tbl.slot_10))
    if user_tbl.slot_12:
      keys.append(str(user_tbl.slot_12))

    res = Session.get_by_key_name(keys)

    for s in res:
      s.curr_ = s.curr_ - 1
      s.put()

    user_tbl.canceld = True
    user_tbl.slot_0 = None
    user_tbl.slot_2 = None
    user_tbl.slot_4 = None
    user_tbl.slot_6 = None
    user_tbl.slot_8 = None
    user_tbl.slot_10 = None
    user_tbl.slot_12 = None
    user_tbl.put()

    path = os.path.join(os.path.dirname(__file__), 'view/routing.html')
    self.response.out.write(template.render(path, {'filename': 'blocks/canceld.html', 'page':'canceld'}))


# done
class RegDonePage(webapp.RequestHandler):
  def post(self):
    user = users.get_current_user()
    if not user:
      loginRequired(self, "/conference/2012/09/reg_program.html")
      return

    user_tbls = getUserTbl(user)
    if not user_tbls:
      self.redirect('/conference/2012/09/reg_top.html')
      return

    user_tbl = user_tbls[0]

    keys = []
    if user_tbl.slot_0:
      keys.append(str(user_tbl.slot_0))
    if user_tbl.slot_2:
      keys.append(str(user_tbl.slot_2))
    if user_tbl.slot_4:
      keys.append(str(user_tbl.slot_4))
    if user_tbl.slot_6:
      keys.append(str(user_tbl.slot_6))
    if user_tbl.slot_8:
      keys.append(str(user_tbl.slot_8))
    if user_tbl.slot_10:
      keys.append(str(user_tbl.slot_10))
    if user_tbl.slot_12:
      keys.append(str(user_tbl.slot_12))

    res = Session.get_by_key_name(keys)

    for s in res:
      s.curr_ = s.curr_ - 1
      s.put()

    name = user_tbl.name
    email = user_tbl.email
    slot_0 = self.request.get('slot_0')
    slot_2 = self.request.get('slot_2')
    slot_4 = self.request.get('slot_4')
    slot_6 = self.request.get('slot_6')
    slot_8 = self.request.get('slot_8')
    slot_10 = self.request.get('slot_10')
    slot_12 = self.request.get('slot_12')

    slot_p0 = self.request.get('slot_p0')
    slot_p2 = self.request.get('slot_p2')
    slot_p4 = self.request.get('slot_p4')
    slot_p6 = self.request.get('slot_p6')
    slot_p8 = self.request.get('slot_p8')
    slot_p10 = self.request.get('slot_p10')
    slot_p12 = self.request.get('slot_p12')

    user_tbl.slot_0 = slot_0
    user_tbl.slot_2 = slot_2
    user_tbl.slot_4 = slot_4
    user_tbl.slot_6 = slot_6
    user_tbl.slot_8 = slot_8
    user_tbl.slot_10 = slot_10
    user_tbl.slot_12 = slot_12

    pflag = False
    if slot_p0:
      pflag = True
      user_tbl.slot_0 = slot_po
    if slot_p2:
      pflag = True
      user_tbl.slot_2 = slot_p2
    if slot_p4:
      pflag = True
      user_tbl.slot_4 = slot_p4
    if slot_p6:
      pflag = True
      user_tbl.slot_6 = slot_p6
    if slot_p8:
      pflag = True
      user_tbl.slot_8 = slot_p8
    if slot_p10:
      pflag = True
      user_tbl.slot_10 = slot_p10
    if slot_p12:
      pflag = True
      user_tbl.slot_12 = slot_p12

    user_tbl.put()

    program = open(os.path.join(os.path.dirname(__file__), 'datas/program.json')).read()
    progdic = simplejson.loads(program)

    sessions_ = {}

    for slot in progdic:
      if "sessions" in slot:
        for session in slot['sessions']:
          sessions_[str(session['session_id'])] = {'title': session['title'], 'timeslot': slot['timeslot']}

    regs = []
    keys = []
    if not pflag:
      if slot_0:
        regs.append(sessions_.get(slot_0))
        keys.append(slot_0)
      if slot_2:
        regs.append(sessions_.get(slot_2))
        keys.append(slot_2)
      if slot_4:
        regs.append(sessions_.get(slot_4))
        keys.append(slot_4)
      if slot_6:
        regs.append(sessions_.get(slot_6))
        keys.append(slot_6)
      if slot_8:
        regs.append(sessions_.get(slot_8))
        keys.append(slot_8)
      if slot_10:
        regs.append(sessions_.get(slot_10))
        keys.append(slot_10)
      if slot_12:
        regs.append(sessions_.get(slot_12))
        keys.append(slot_12)

    if pflag:
      if slot_p0:
        regs.append(sessions_.get(slot_p0))
        keys.append(slot_p0)
      if slot_p2:
        regs.append(sessions_.get(slot_p2))
        keys.append(slot_p2)
      if slot_p4:
        regs.append(sessions_.get(slot_p4))
        keys.append(slot_p4)
      if slot_p6:
        regs.append(sessions_.get(slot_p6))
        keys.append(slot_p6)
      if slot_p8:
        regs.append(sessions_.get(slot_p8))
        keys.append(slot_p8)
      if slot_p10:
        regs.append(sessions_.get(slot_p10))
        keys.append(slot_p10)
      if slot_p12:
        regs.append(sessions_.get(slot_p12))
        keys.append(slot_p12)

    res = Session.get_by_key_name(keys)

    for s in res:
      s.curr_ = s.curr_ + 1
      if s.curr_ < s.max_ * 2 / 3:
        s.status = "ok"
      if s.curr_ > s.max_ * 2 / 3:
        s.status = "jam"
      if s.curr_ > s.max_:
        s.status = "full"
      s.put()



    mail.send_mail(sender="noreply@html5j.org",
      to = email,
      subject = "登録ありがとうございます",
      body = """
      HTML5 Conference2012への登録まことにありがとうございます
      お客様の登録状況は以下のとおりです

      hogehoge...
      """)
    path = os.path.join(os.path.dirname(__file__), 'view/reg_done.html')
    self.response.out.write(template.render(path, {'page':'reg_done', 'name': name, 'email': email, 'registration': regs}))



"""
routing part
"""
def main():

  application = webapp.WSGIApplication([
    ('/conference/2012/09/', MainPage),
    ('/conference/2012/09/index.html', MainPage),
    # ('/conference/2012/09/sponsor.html', SponsorPage),
    # ('/conference/2012/09/volunteer.html', VolunteerPage),
    ('/conference/2012/09/program.html', ProgramPage),
    ('/conference/2012/09/speaker.html', SpeakerPage),
    ('/conference/2012/09/faq.html', FaqPage),
    ('/conference/2012/09/reg_top.html', RegTopPage),
    ('/conference/2012/09/reg_program.html', RegProgramPage),
    # ('/conference/2012/09/reg_confirm.html', RegConfirmPage),
    ('/conference/2012/09/reg_done.html', RegDonePage),
    ('/conference/2012/09/cancel_done.html', CancelDonePage)
 ], debug=True)
  wsgiref.handlers.CGIHandler().run(application)

"""
invoke main()
"""
if __name__ == '__main__':
  main()
