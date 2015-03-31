import os
import cgi
from google.appengine.ext import ndb
import json
import jinja2
import webapp2


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)
	
class User(ndb.Model):
    """Sub model for storing user activity.""" 
    name = ndb.StringProperty(indexed=True)
    emailid = ndb.StringProperty(indexed=True)
    pin = ndb.StringProperty(indexed=True)
   	
class Response(ndb.Model):
    """Sub model for representing question details"""
    useremailid = ndb.StringProperty(indexed = True)
    qid = ndb.StringProperty(indexed = True)
    ans = ndb.StringProperty(indexed = True)
    qshowntime = ndb.StringProperty(indexed = True)
    qattemptedtime = ndb.StringProperty(indexed = True)
    score = ndb.StringProperty(indexed = True)

class MainPage(webapp2.RequestHandler):

    def get(self):        
        template = JINJA_ENVIRONMENT.get_template('taketest.html')
        self.response.write(template.render())

class Result(webapp2.RequestHandler):
    def get(self):
        jdata = json.loads(cgi.escape(self.request.body))
        for vals in jdata:
            useremailid = vals['useremailid']
        q = User.query(User.emailid == useremailid ).get()
        if q:
            q1=Response.query().get()
        if q1:
            self.response.content_type = 'application/json'
            obj = {
					'qid': 'q1.qid',
					'ans': 'q1.ans',
					'score': 'q1.score',
					'section': 'q1.section',
					'qshowntime' : 'q1.qshowntime',
					'qattemptedtime': 'q1.qattemptedtime'
				}
            self.response.write(json.encode(obj))

class submit(webapp2.RequestHandler):
    def get(self):
        vals = json.loads(cgi.escape(self.request.get('jsonData')))
        useremailid = vals['useremailid']
        qid = vals['qid']
        ans = vals['ans']
        qshowntime = vals['qshowntime']
        qattemptedtime = vals['qattemptedtime']
        score = vals['score']
        data=Response(useremailid=useremailid,qid=qid+"",ans=ans,qshowntime=qshowntime,qattemptedtime=qattemptedtime,score=score)
        data.put()

application = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/submitanswer', submit),
       ], debug=True)