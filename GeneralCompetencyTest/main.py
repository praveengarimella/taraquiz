import os

from google.appengine.api import mail
from google.appengine.api import users
from google.appengine.ext import ndb
from webapp2_extras import json
import jinja2
import webapp2


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class Main(webapp2.RequestHandler):
    def get(self):
		  template = JINJA_ENVIRONMENT.get_template('taketest.html')
                self.response.write(template.render())

class Result(webapp2.RequestHandler):
    def get(self):
		jdata = json.loads(cgi.escape(self.request.body))
		for vals in jdata:
			useremailid = vals['useremailid']
		q=user.query(user.emailid=useremailid).get()
		if q:
			q1=response.query().get()
			if q1:
				self.response.content_type = 'application/json'
				obj = {
					'qid': 'q1.qid', 
					'ans': 'q1.ans',
					'score': 'q1.score',
					'section': 'q1.section',
					'qshowntime' : 'q1.qshowntime'
					'qattemptedtime' : 'q1.qattemptedtime'
				} 
				self.response.write(json.encode(obj))
			
class submit(webapp2.RequestHandler):
    def get(self):
        jdata = json.loads(cgi.escape(self.request.body))
		for vals in jdata:
			useremailid = vals['useremailid']
			qid = vals['qid']
			ans = vals['ans']
			qshowntime = vals['qshowntime']
			qattemptedtime = vals['qattemptedtime']
			score = vals['score']
			section = vals['section']
		q=user.query(user.emailid=useremailid).get()
		if q:
		data=response(section=section,useremailid=useremailid,qid=qid,ans=ans,qshowntime=qshowntime,qattemptedtime=qattemptedtime,score=score)
		data.put()

application = webapp2.WSGIApplication([
    ('/', Main),
	('/submitanswer', submit),
	('/showresult', Result ),
  ], debug=True)