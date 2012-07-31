#!-*- coding:utf-8 -*-

import wsgiref.handlers
import os
#from attend import Attend, AttendForm
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
#from google.appengine.api import mail
#from google.appengine.api import users

g_regist=True

"""
Topページ
"""
class MainPage(webapp.RequestHandler):
  def get(self):
    path = os.path.join(os.path.dirname(__file__), 'view/index.html')
    self.response.out.write(template.render(path, {'page':'index'}))

"""
登録ページ
getの時は登録フォーム(view/registration.html)が、POSTの時は登録内容の確認画面(view/confirm.html)が表示される
"""
class RegistrationPage(webapp.RequestHandler):
  def get(self):
    path = os.path.join(os.path.dirname(__file__), 'view/registration.html')
    self.response.out.write(template.render(path, {'page':'registration', 'regist':g_regist}))

"""
隠し登録ページ
"""
class HiddenPage(webapp.RequestHandler):
  def get(self):
    path = os.path.join(os.path.dirname(__file__), 'view/hiddenreg.html')
    self.response.out.write(template.render(path, {'page':'hiddenreg', 'regist':g_regist}))

"""
隠し登録ページ
"""
class SecretPresentPage(webapp.RequestHandler):
  def get(self):
    path = os.path.join(os.path.dirname(__file__), 'view/secret-present.html')
    self.response.out.write(template.render(path, {'page':'secret-present'}))

"""
プログラムのページ
program_のマップオブジェクトより、サーバーサイドでレンダリングされる
"""
class ProgramPage(webapp.RequestHandler):
  def get(self):

    program_ = {
    "A":[
      {"timetable":"10:00-10:45","description":"HTML5と関連APIにおける意義と概要を、ポイントを絞って紹介します。セッションの前半はW3C深見さんにお越しいただき、普段なかなか接することのない「W3Cの視点」から標準を語っていただきます。","speaker":"深見 嘉明 (W3C/Keio)<br>白石 俊平 (HTML5 Developers JP)","name":"HTML5/Web標準オーバービュー","slide":"http://www.slideshare.net/shumpei/html5web","movie":"http://www.youtube.com/user/HTML5DevelopersJP?feature=mhee#p/u/5/Cl4zr1OyuOg"},
      {"timetable":"11:00-11:45","description":"HTML5のマークアップの特徴を一言で表すとすれば「セマンティクス」。それ故に、HTML5では文脈に合わせてマークアップしなければいけません。もはや、マークアップは単純作業ではなくクリエイティブなものになっているのです。マークアップにも心得と作法がよりいっそう重要になってきています。本セッションでは、HTML5仕様ではマークアップに何を求めているのか（心得）、そして、我々はどのようにマークアップをすべきか（作法）、について具体的に解説します。","speaker":"羽田野 太巳 (futomi)","name":"HTML5マークアップの心得と作法","slide":"http://www.slideshare.net/futomihatano/html5-9066829","movie":"http://www.youtube.com/user/HTML5DevelopersJP?feature=mhee#p/u/3/0l3ZyW8SKR8"},
      {"timetable":"13:00-13:45","description":"CSS3を使うと、従来は組むのが大変だったデザインや、JSが必要だったアニメーションなどを簡単に実装することができます。モバイルデバイスなどのしかし一方でCSS3に対応してないブラウザのことを考えるとまだ使うのに尻込みしてしまうこともあるかと思います。このセッションでは、Graceful Degradationの考え方を導入しながら、ウェブデザインの中で実際にどんな風にCSS3を使っていけばいいかを紹介します。","speaker":"小久保 浩大郎 (グーグル株式会社)","name":"実践CSS3デザイン","movie":"http://www.youtube.com/user/HTML5DevelopersJP?feature=mhee#p/u/4/YozA0LF5p-4"},
      {"timetable":"14:00-14:45","description":"スマートフォンのブラウザは小さなディスプレイ、ネットワークの遅さなど、ページを作るにあたり、色々考慮しなくてはいけないことがあります。このセッションでは綺麗で高速なスマートフォンに最適化されたサイトを作るためのノウハウやツールを紹介します。","speaker":"Yuji Sunouchi (グーグル株式会社)","name":"スマートフォン向け開発","movie":"http://www.youtube.com/user/HTML5DevelopersJP?feature=mhee#p/u/1/zweWBc_3v6Y"},
      {"timetable":"15:00-15:45","description":"HTML5の注目ともに、ブラウザの対応状況などの効果も相まって、SVGも再注目されてきています。<br>基礎編と応用編に分け、基礎編ではSVGを全く知らない人でも一からSVGがわかるように、SVGの特徴や基本的な記述などについて解説します。<br>応用編ではSVGを使ったインタラクティブなコンテンツやUIを作るためのアニメーションやフィルターなど、少し高度なSVGの技術について紹介します。","speaker":"外村 和仁 (株式会社ピクセルグリッド)<br>小山田 晃浩 (株式会社ピクセルグリッド)","name":"Dive into SVG","slide":"http://www.slideshare.net/yomotsu/dive-into-svg","movie":"http://www.youtube.com/user/HTML5DevelopersJP?feature=mhee#p/u/0/Im0ua46TRMk","demo":"http://demo.pxgrid.com/svg/demo/index.html"},
      {"timetable":"16:00-16:45","description":"HTML5の実装が進んでいる中、多様なブラウザに対しどのように対応していくかが課題となっています。このセッションでは、いくつかの対応指針を紹介したうえで、Modernizrとpolyfillsを使ったRegressive Enhancementという考え方について説明します。","speaker":"矢倉 眞隆","name":"今から使える!? HTML5","slide":"http://dl.dropbox.com/u/130643/crhtml5/slides.html#1","movie":"http://www.youtube.com/user/HTML5DevelopersJP?feature=mhee#p/u/2/QKrbRfjXo-g"}
      ],
    "B":[
      {"timetable":"10:00-10:45","description":"ウェブアプリはこれまで標準的な課金や周知の手段がなく、一部サイトを除き収入のほとんどを広告収入に依るしかないのが現実でした。Chrome Web Storeはそういった状況を一変させ、ウェブを受益者負担の健全なアプリケーションプラットフォームへと生まれ変わらせてくれる可能性があります。本セッションではChrome Web Storeについて、なにが新しいのか、なにができるのか、どうやればいいのか、などについて説明し、Googleの考える未来のウェブを第三者の視点から考察します。","speaker":"あんどうやすし (mixi)","name":"Chrome Web Store入門","slide":"https://docs.google.com/present/view?id=dchb3tb2_263dkg7d2ht","movie":"http://www.youtube.com/watch?v=ULLYD3kyynI#t=55m20s","commentary":"http://d.hatena.ne.jp/technohippy/20110824#1314209267"},
      {"timetable":"11:00-11:45","description":"フロント開発のデバッグツールは今のままで十分ですか？Chrome Developer Toolsも試してみてください！このセッションではChrome Developer Toolsのエッセンスをご紹介します。","speaker":"北村 英志 (グーグル株式会社)","name":"Debugging on Chrome Developer Tools!","movie":"http://www.youtube.com/watch?v=ULLYD3kyynI#t=1h52m00s"},
      {"timetable":"13:00-13:45","description":"Webアプリの可能性を飛躍的に向上すると話題のWebSocket。Webでのリアルタイムサービスが可能になります。一方で、通信プロトコルという分かりづらい部分の新たなAPIのため、全体像を掴みづらいのも事実です。そんなWebSocketをメインに、HTML5のコミュニケーション系APIにより「何が変わるのか？」「どんなメリットが得られるのか？」具体的なWebアプリを用い紹介します。","speaker":"小松 健作 (NTTコミュニケーションズ)","name":"WebSocketでリアルタイム通信","slide":"http://www.slideshare.net/KensakuKOMATSU/websocket-8910998","movie":"http://www.youtube.com/watch?v=ULLYD3kyynI#t=3h49m18s!"},
      {"timetable":"14:00-14:45","description":"5月リリースした、Chrome ウェブアプリ「はてなブックマーク」がどのようにHTML5のAPI活用し、どういったフローで開発したか担当ディレクターとエンジニアが解説します。","speaker":"長山 武史 (はてなブックマーク ディレクター)<br>外山 真 (はてなブックマーク エンジニア)","name":"ウェブアプリの道も一歩から ～はてなブックマークの場合～","slide":"http://www.slideshare.net/nagayama/web-8984239","movie":"http://www.youtube.com/watch?v=ULLYD3kyynI#t=4h49m35s","commentary":"http://d.hatena.ne.jp/hatenatech/20110826/1314338430"},
      {"timetable":"15:00-15:45","description":"ユーザーは高機能で使いやすく、高速なウェブアプリを望んでいます。現実にそれらすべてを満たすことは極めて困難な課題といえるでしょう。しかし、高速化についてはいくつかのポイントを抑えるだけで劇的な改善が望めます。本セッションでは、ライブコーディングを行いながら、ウェブアプリの高速化テクニックをChrome Developer Toolsで実証しながら紹介していきます。","speaker":"太田 昌吾 (クックパッド)","name":"実践・ウェブアプリ高速化テクニック","slide":"http://ss-o.net/event/20110821/","movie":"http://www.youtube.com/watch?v=ULLYD3kyynI#t=5h48m52s"},
      {"timetable":"16:00-16:45","description":"Publickeyの新野淳一さんを司会に、HTML5最前線の人たちによるパネルディスカッション。","speaker":"新野 淳一 (Publickey)<br>及川 卓也 (グーグル株式会社)<br>白石 俊平 (HTML5 Developers JP)<br><s>川島 優志 (グーグル株式会社)</s><br>小久保 浩大郎 (グーグル株式会社)<br>深見 義明 (W3C/Keio)","name":"HTML5パネルディスカッション","movie":"http://www.youtube.com/watch?v=ULLYD3kyynI#t=6h49m22s"}
      ],
    "HandsOn":[{"timetable":"13:00-14:45","description":"CanvasとSVGを通してJavaScriptコーディングを体験する初心者向けハンズオンです。ひとつの題材を、Canvasで作るチームとSVGで作るチームに分かれて、時間内に作って頂きます。コーディングの前にはCanvasとRaphaelの使い方を簡単に説明します。SVGでは、XMLマークアップではなく、RaphaelというJSライブラリーを使ったJavaScriptコーディングを行って頂きます。このハンズオンを通して、それぞれのテクノロジーの違いについても理解することができるでしょう。","speaker":"羽田野 太巳 (futomi)","name":"JavaScript初心者のためのSVG／Canvasアニメーション入門"},
      {"timetable":"15:00-16:45","description":"CSS3+JavaScriptでユーザー入力フォーム画面を作成する、CSS3&JavaScript初心者向けハンズオンです。<br>コーディングは各個人のペースで進めていただきます。<br>前半：CSS3を使ってのUIパーツ作り、少量のJavaScriptで動きを出すコーディングの解説と練習<br>後半：UIパーツを組み合わせて、ユーザー入力フォーム画面コーディングにチャレンジ<br>この内容を通して定番のデザイン、アニメーションなど体験します。合わせて、少しのJavaScript追加でスムーズなUIパーツができることを知っていただくことができるでしょう。","speaker":"一條 美和子 (産経デジタル)","name":"CSS3のハンズオン"}
      ],"LT":[{"timetable":"17:30-18:30","description":"N/A","speaker":"モデレータ：河内典子 (アイティメディア)","name":"ライトニングトーク"}],"Keynote":[{"timetable":"9:30-10:00","description":"N/A","speaker":"及川 卓也 (グーグル株式会社)","name":"基調講演"}]}

    path = os.path.join(os.path.dirname(__file__), 'view/program.html')
    self.response.out.write(template.render(path, {'page':'program', 'data':0, 'program':program_}))

"""
FAQのページ
"""
class Faq(webapp.RequestHandler):
  def get(self):

    path = os.path.join(os.path.dirname(__file__), 'view/faq.html')
    self.response.out.write(template.render(path, {'page':'faq'}))

"""
不参加の方向けのページ
"""
class Nonparticipant(webapp.RequestHandler):
  def get(self):
    path = os.path.join(os.path.dirname(__file__), 'view/nonparticipant.html')
    self.response.out.write(template.render(path, {'page':'nonparticipant'}))

"""
登録状況の確認。debug用。未使用
"""
class AttendeesPage(webapp.RequestHandler):
  def get(self):
    attendees = Attend.gql("where removeflag = False")
    data = {'attendees':attendees, 'page':'attendees'}
    path = os.path.join(os.path.dirname(__file__), 'view/attendees.html')
    self.response.out.write(template.render(path, data))

"""
登録削除の確認。debug用。未使用
"""
class DeleteConfirmPage(webapp.RequestHandler):
  def post(self, id):
    attend = Attend.get_by_id(int(id))
    data = {'name':attend.name,
        'nickname': attend.nickname,
        'email' : attend.email,
        'id': id}
    path = os.path.join(os.path.dirname(__file__), 'view/delete_confirm.html')
    self.response.out.write(template.render(path, data))

"""
登録削除。debug用。未使用
"""
class DeletePage(webapp.RequestHandler):
  def post(self, id):
    attend = Attend.get_by_id(int(id))
    attend.removeflag = True
    attend.put()
    self.redirect('/attendees.html')

"""
確認ページ（confirm.html)で、「登録」をクリックすると呼び出される
登録内容をDBに登録する。また、thank youメールを送信する。
"""
class SubscribePage(webapp.RequestHandler):
  def post(self):
    # template html
    path = os.path.join(os.path.dirname(__file__), 'view/subscribe.html')

    # 入力パラメータの取得
    name = self.request.POST['name']
    nickname = self.request.POST['nickname']
    email = self.request.POST['email']

    # thank you メールを送信
    mail.send_mail(sender="kensaku.komatsu@gmail.com",
        to=email,
        subject="Thank you for your attendee",
        body="Thank you!!")

    # DBに登録する
    attend = Attend(name=name, nickname=nickname, email=email)
    attend.put()

    # 登録完了が面を表示
    self.response.out.write(template.render(path, {}))

class Redirect(webapp.RequestHandler):
  def get(self):
    self.redirect('/conference/2011/08/')


class MyHandler(webapp.RequestHandler):
  def get(self):
    user = users.get_current_user()
    if user:
      greeting = ("Welcome, %s! (<a href=\"%s\">sign out</a>)" %
                  (user.nickname(), users.create_logout_url("/intl/ja/")))
    else:
      greeting = ("<a href=\"%s\">Sign in or register</a>." %
                  users.create_login_url("/intl/ja/"))

    self.response.out.write("<html><body>%s</body></html>" % greeting)

"""
Mainのルーティング部
"""
def main():
  application = webapp.WSGIApplication([
#    ('/', Redirect),
    ('/conference/2011/08/', MainPage),
    ('/conference/2011/08/index.html', MainPage),
    ('/conference/2011/08/program.html',ProgramPage),
    ('/conference/2011/08/registration.html', RegistrationPage),
    ('/conference/2011/08/hiddenreg.html', HiddenPage),
#    ('/attendees.html', AttendeesPage),
#    ('/delete_confirm/(¥d)/', DeleteConfirmPage),
#    ('/delete/(¥d)/', DeletePage),
    ('/conference/2011/08/subscribe.html', SubscribePage),
    ('/conference/2011/08/faq.html', Faq),
    ('/conference/2011/08/nonparticipant.html', Nonparticipant),
    ('/conference/2011/08/secret-present.html', SecretPresentPage)
    ], debug=True)
  wsgiref.handlers.CGIHandler().run(application)

"""
main()のinvoke
"""
if __name__ == '__main__':
  main()
