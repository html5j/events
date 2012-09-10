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
import hashlib
import uuid
import logging
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


"""
Entry Model
"""
class EntryLogs(db.Model):
  created = db.DateTimeProperty(auto_now_add=True)
  log = db.StringProperty(required=True)

"""
MailBody Model
"""
class MailBodies(db.Model):
  # body = db.StringProperty(multiline=True, required=True)
  body = db.TextProperty(required=True)

"""
Inquiry Model
"""
class Inquiries(db.Model):
  data = db.TextProperty(required=True)




"""
Utlitilities
"""
def getCurrentNum():
  # get rid of db procedure
  return 999
  # q =  Users.all()
  # q.filter('canceld =', False)

  # return len(q.fetch(1100))



def canSubscribe():
  max_ = 999

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
    sponsorsJsonFile = open(os.path.join(os.path.dirname(__file__), 'datas/sponsors.json')).read()
    sponsors = simplejson.loads(sponsorsJsonFile)

    path = os.path.join(os.path.dirname(__file__), 'view/index.html')
    self.response.out.write(template.render(path, {'page':'index', 'can_subscribe': canSubscribe(), 'sponsors': sponsors }))

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
Inquiry page
"""
class InquiryPage(webapp.RequestHandler):
  def get(self):
    program = open(os.path.join(os.path.dirname(__file__), 'datas/program.json')).read()
    progdic = simplejson.loads(program)

    slot_ids = [2,4,6,8,10]

    path = os.path.join(os.path.dirname(__file__), 'view/routing.html')
    uuid_ = str(uuid.uuid1())
    self.response.out.write(template.render(path, {'filename': 'blocks/inquiry.html', 'id': uuid_, 'page':'inquiry', 'progdic': progdic, 'slot_ids': slot_ids}))
  def post(self):
    path = os.path.join(os.path.dirname(__file__), 'view/routing.html')
    uuid_ = str(uuid.uuid1())

    # check post parameters
    id = self.request.get('id')
    data = self.request.get('data')

    logging.info("id : %s", id)

    inquiry = Inquiries(key_name = id, data = data)
    inquiry.put()

    # self.response.out.write(template.render(path, {'filename': 'blocks/inquiry.html', 'id': uuid_, 'page':'inquiry'}))
    self.redirect('/conference/2012/09/inquiry.html')

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
    # self.response.out.write(template.render(path, {'filename': 'blocks/program.html', 'sess': getSessions(), 'page':'program', 'program': program, 'progdic': progdic, 'speadic': speadic}))
    self.response.out.write(template.render(path, {'filename': 'blocks/program.html', 'sess': None, 'page':'program', 'program': program, 'progdic': progdic, 'speadic': speadic}))

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
    self.response.out.write(template.render(path, {'filename': 'blocks/speaker.html', 'page':'speaker', 'program': program, 'progdic': progdic, 'speadic': speadic, 'currentNum': getCurrentNum() }))

"""
article's page
"""

class ArticlesPage(webapp.RequestHandler):
  def get(self):
    reportersJSON = open(os.path.join(os.path.dirname(__file__), 'datas/reporters.json')).read()
    reporters = simplejson.loads(reportersJSON)
    path = os.path.join(os.path.dirname(__file__), 'view/routing.html')
    self.response.out.write(template.render(path, {'filename': 'blocks/articles.html', 'page': 'articles', 'reporters': reporters }))


"""
faq page
"""
class FaqPage(webapp.RequestHandler):
  def get(self):
    path = os.path.join(os.path.dirname(__file__), 'view/routing.html')
    self.response.out.write(template.render(path, {'filename': 'blocks/faq.html', 'page':'faq'}))

"""
access page
"""
class AccessPage(webapp.RequestHandler):
  def get(self):
    path = os.path.join(os.path.dirname(__file__), 'view/routing.html')
    self.response.out.write(template.render(path, {'filename': 'blocks/access.html', 'page':'access'}))

"""
map page
"""
class MapPage(webapp.RequestHandler):
  def get(self):
    path = os.path.join(os.path.dirname(__file__), 'view/routing.html')
    self.response.out.write(template.render(path, {'filename': 'blocks/map.html', 'page':'map'}))

"""
registration pages
"""
#class RedirectPage(webapp.RequestHandler):
def loginRequired(self, page):
  str = (u"<a href=\"%s\">Google アカウントで login する</a>" % users.create_login_url(page))
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
      user_tbl.slot_0 = slot_p0
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

    """
    logging Entry log
    """
    mesg = ",".join([
      hashlib.sha1(str(user_tbl.email)).hexdigest(),
      user_tbl.slot_0,
      user_tbl.slot_2,
      user_tbl.slot_4,
      user_tbl.slot_6,
      user_tbl.slot_8,
      user_tbl.slot_10,
      user_tbl.slot_12
    ])

    entry = EntryLogs(log = mesg)
    entry.put()

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

    contents = "     =============================\n"
    for session in regs:
      contents += "     "+session['timeslot']+"\n"
      contents += "     "+session['title']+"\n"
    contents += "     =============================\n"
    id = hashlib.sha1(email).hexdigest()

    body = """
    本メールは、HTML5 Conference 2012 にお申込みいただいた方々にお送りしております。

    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    HTML5 Conference 2012 参加証のご案内
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    """

    body += "     "+name.encode('UTF-8')+" 様\n\n"

    body += "     登録ID："+id+"\n\n"

    body += """

    ■ 登録内容
"""
    body += contents.encode('UTF-8')

    body += """

    この度は、「HTML5 Conference 2012」にお申込みいただきまして、誠にありがとうございます。

    当日は受付に本メールのプリントアウトしたもの、またはスマートフォンの画面をご提示ください。


    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    HTML5 Conference 2012 ご来場について
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

    ■イベント概要
    開催日
      2012年 9月8日 (土)　11:00 - 19:30 (受付開始 10:30)
      主催
        html5j.org
      募集人数
        1,000名
      会場
        慶應義塾大学 日吉キャンパス 協生館 (神奈川県横浜市港北区日吉4-1-1)
      アクセス
        以下のサイトをご覧いただき、ご来場ください。
            http://www.kcc.keio.ac.jp/access/index.html
            http://goo.gl/maps/aas5
      参加費
        無料


      ■ 受付について
        ・イベント当日、本メールにて参加証の確認を行いますので、プリントアウトしていただくか、スマートフォンなどの画面をご提示ください。
        ・当日は受付が混雑することが予想されます。時間に余裕を持ってお越しください。

      [注意事項]
        ・参加証に記載されたご本人さまのみ参加することができます。
          代理での出席やご本人様以外の方がお越しになられた場合、ご入場することができません。
          なお、本人確認ができるものをご提示できない場合、ご入場をお断りする場合があります。

      ■ 個人Wi-Fi機器の使用に関して
        ・当日会場内では無線LANの提供を行う予定です。
          つきましては、会場の無線機器と干渉してしまいますので、ご使用は控えていただけますようご協力お願いいたします。

      ■ 飲食について
        ・当日の昼休み（12:45）までに受付をされた方には、慶應義塾大学構内の学生食堂で利用できるチケット（500円分）を配布いたします。
        ・セッションが行われる会場(大ホール・各教室)は飲食禁止となっております。
          お飲み物を飲まれる際にはホールの外、または廊下をご利用ください。

      ■ その他
        ・電源について
          大ホール1階の各座席にて電源がご利用できます。
          多目的教室1〜3については若干数の電源を用意する予定です。

          不明な点などございましたら、下記のフォームからお問い合わせください。
             http://goo.gl/NCnmg


     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        HTML5 Conference 2012 ウェブサイト：http://events.html5j.org/conference/2012/09/
        html5j.org ウェブサイト：http://www.html5j.org/
        html5j.org Googleグループ：http://goo.gl/T6hoV

"""

    #body = open(os.path.join(os.path.dirname(__file__), 'datas/mail.txt')).read()

    #body.encode('UTF-8').replace('{rName}', name)



    mail.send_mail(sender="event@html5j.org",
      to = email,
      subject = "登録ありがとうございます",
      body = body)
    path = os.path.join(os.path.dirname(__file__), 'view/reg_done.html')
    self.response.out.write(template.render(path, {'page':'reg_done', 'body': body, 'name': name, 'email': email, 'registration': regs}))

"""
Reminder page
"""
class ReminderPage(webapp.RequestHandler):
  def get(self):
    user = users.get_current_user()
    if not user:
      loginRequired(self, "/conference/2012/09/reminder.html")
      return

    logging.info("reminder page has acccessed by %s", user.email())

    if not user.email() == 'kensaku.komatsu@gmail.com':
      self.response.out.write("you are not permitted to access this page.")
      return

    path = os.path.join(os.path.dirname(__file__), 'view/reminder.html')
    generic = MailBodies.get_by_key_name('generic', None)
    vip = MailBodies.get_by_key_name('vip', None)

    if generic is None:
      generic_body = ""
    else:
      generic_body = generic.body

    logging.debug(vip)

    if vip is None:
      vip_body = ""
    else:
      vip_body = vip.body

    self.response.out.write(template.render(path, {
      'title':'remider送信ページ（管理者用）',
      'generic_body':generic_body,
      'vip_body' :vip_body
      }))

  def post(self):
    user = users.get_current_user()
    if not user.email() == 'kensaku.komatsu@gmail.com':
      self.response.out.write("you are not permitted to access this page.")
      return

    target = self.request.get('target')
    name = self.request.get('name')
    email = self.request.get('email')

    mail_body = MailBodies.get_by_key_name(target)

    if mail_body:
      body = mail_body.body
    else:
      body = ""

    body_ = body.replace("{{name}}", name).replace("{{email}}", email)

    if target == "generic":
      logging.info("getting registration info for generic subscribers");
      query = Users.all()
      query.filter('email =', email)
      res = query.fetch(1)

      program = open(os.path.join(os.path.dirname(__file__), 'datas/program.json')).read()
      progdic = simplejson.loads(program)

      sessions_ = {}

      for slot in progdic:
        if "sessions" in slot:
          for session in slot['sessions']:
            sessions_[str(session['session_id'])] = {'title': session['title'], 'timeslot': slot['timeslot']}

      regs = []

      if res[0].slot_0:
        regs.append(sessions_[res[0].slot_0])
      if res[0].slot_2:
        regs.append(sessions_[res[0].slot_2])
      if res[0].slot_4:
        regs.append(sessions_[res[0].slot_4])
      if res[0].slot_6:
        regs.append(sessions_[res[0].slot_6])
      if res[0].slot_8:
        regs.append(sessions_[res[0].slot_8])
      if res[0].slot_10:
        regs.append(sessions_[res[0].slot_10])
      if res[0].slot_12:
        regs.append(sessions_[res[0].slot_12])

      contents = "     =============================\n"

      for session in regs:
        contents += "     "+session['timeslot']+"\n"
        contents += "     "+session['title']+"\n"

      contents += "     =============================\n"
      id = hashlib.sha1(email).hexdigest()

      body_ = body_.replace("{{contents}}", contents).replace("{{id}}", id)


    logging.info("Sent %s mail to: email = %s, name = %s, target = %s", target, email, name, target)

    mail.send_mail(sender="event@html5j.org",
      to = email,
      subject = "[HTML5 Conference 2012]参加証の送付",
      body = body_)

    self.response.out.write(simplejson.dumps({"target": target, "name": name, "email": email, "body": body_}))


"""
APIs
"""
class MailBodyAPI(webapp.RequestHandler):
  def post(self):
    user = users.get_current_user()
    if not user.email() == 'kensaku.komatsu@gmail.com':
      self.response.out.write("you are not permitted to access this page.")
      return

    target = self.request.get('target')
    body = self.request.get('body')
    logging.debug(target+", "+body)

    mail_body = MailBodies(key_name = target, body = body)
    mail_body.put()


    self.response.headers['Content-Type'] = "application/json"
    self.response.out.write(simplejson.dumps({"target":target , "body": body}))

class SubscriberAPI(webapp.RequestHandler):
  def get(self):
    user = users.get_current_user()
    if not user.email() == 'kensaku.komatsu@gmail.com':
      self.response.out.write("you are not permitted to access this page.")
      return

    q =  Users.all()
    q.filter('canceld =', False)
    subscribers = q.fetch(1100)

    ret = []
    for subscriber in subscribers:
      ret.append({"email": subscriber.email, "name": subscriber.name})

    self.response.headers['Content-Type'] = "application/json"
    self.response.out.write(simplejson.dumps(ret))


"""
routing part
"""
def main():
  logging.getLogger().setLevel(logging.DEBUG)

  application = webapp.WSGIApplication([
    ('/conference/2012/09/', MainPage),
    ('/conference/2012/09/index.html', MainPage),
    # ('/conference/2012/09/sponsor.html', SponsorPage),
    # ('/conference/2012/09/volunteer.html', VolunteerPage),
    ('/conference/2012/09/program.html', ProgramPage),
    ('/conference/2012/09/speaker.html', SpeakerPage),
    ('/conference/2012/09/articles.html', ArticlesPage),
    ('/conference/2012/09/faq.html', FaqPage),
    ('/conference/2012/09/access.html', AccessPage),
    ('/conference/2012/09/map.html', MapPage),
    # ('/conference/2012/09/reg_top.html', RegTopPage),
    # ('/conference/2012/09/reg_program.html', RegProgramPage),
    # ('/conference/2012/09/reg_confirm.html', RegConfirmPage),
    # ( '/conference/2012/09/reg_done.html', RegDonePage),
    # ('/conference/2012/09/cancel_done.html', CancelDonePage),
    #('/conference/2012/09/lt.html', LtPage),
    #('/conference/2012/09/writer.html', WriterPage),
    # ('/conference/2012/09/inquiry.html', InquiryPage),
    # ('/conference/2012/09/reminder.html', ReminderPage),
    # ('/conference/2012/09/mail_body', MailBodyAPI),
    # ('/conference/2012/09/subscriber', SubscriberAPI)
 ], debug=True)
  wsgiref.handlers.CGIHandler().run(application)

"""
invoke main()
"""
if __name__ == '__main__':
  main()
