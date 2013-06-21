import cgi
import os

from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app

class Racer(db.Model):
    name = db.StringProperty()
    email = db.StringProperty()
    phone = db.StringProperty()
    captain = db.StringProperty(choices=set(["on", "off"]), default="off")
    crewcount = db.StringProperty()
    date = db.DateTimeProperty(auto_now_add=True)

class MainPage(webapp.RequestHandler):
    def get(self):
        template_values = {}
        path = os.path.join(os.path.dirname(__file__), "index.html")
        self.response.out.write(template.render(path, template_values))

class RegForm(webapp.RequestHandler):
    def get(self):

        greeting = Racer()
        greeting.name = self.request.get('name')
        greeting.email = self.request.get('email')
        greeting.phone = self.request.get('phone')
        greeting.captain = self.request.get('captain')
        greeting.crewcount = self.request.get('crewcount')
        greeting.put()
        self.redirect('/#reg')

class RacerList(webapp.RequestHandler):
    def get(self):
        greetings = db.GqlQuery("SELECT * FROM Racer ORDER BY date")
        self.response.headers['Content-Type'] = 'text/plain'
        for greeting in greetings:
            self.response.out.write("%s\n" % cgi.escape(greeting.name))
        self.response.out.write("---")

application = webapp.WSGIApplication([("/", MainPage),
                                ("/reg", RegForm),
                                ("/list", RacerList)],
                                debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()