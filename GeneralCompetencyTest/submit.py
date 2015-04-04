import os
import cgi
from google.appengine.ext import ndb
import json
import jinja2
import webapp2
import logging
from pprint import pprint


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
    useremailid = ndb.StructuredProperty(User)
    submittedans = ndb.StringProperty(indexed = True)
    responsetime = ndb.FloatProperty(indexed = True)
    q_score = ndb.IntegerProperty(indexed = True)
    q_status = ndb.StringProperty(indexed = True)
    time = ndb.DateTimeProperty(auto_now_add=True)
    currentQuestion=ndb.StringProperty(indexed = True)

class EssayTypeResponse(ndb.Model):
    """Sub model for storing user response for essay type questions"""
    useremailid = ndb.StringProperty(indexed = True)
    qid = ndb.StringProperty(indexed = True)
    ansText = ndb.StringProperty(indexed = True)
    qshowntime = ndb.StringProperty(indexed = True)
    qattemptedtime = ndb.StringProperty(indexed = True)
    status = ndb.StringProperty(indexed = True)

class audio(ndb.Model):
    mp3 = ndb.BlobProperty()
    date 	= ndb.DateTimeProperty(auto_now_add=True)
    
class MainPage(webapp2.RequestHandler):

    def get(self):
        template = JINJA_ENVIRONMENT.get_template('quiz.html')
        self.response.write(template.render())


class checkuser(webapp2.RequestHandler):
    def get(self):
        data=[]
        data = json.loads(cgi.escape(self.request.get('jsonData')))
        if User.query(User.emailid==data['email']).get() is not None :
            obj = {u"status": "UnSuccessful", u"errorcode":0, u"errormessage":"The Email is invalid"}
        else :
            u1=User(name=data['name'],emailid=data['email'],pin=data['pin'])
            u1.put();
            obj = {u"status": "Successful", u"errorcode":1, u"errormessage":""}

        ss=json.dumps(obj)
        self.response.headers['Content-Type']='application/json'
        self.response.write(ss)
    
class signpage(webapp2.RequestHandler):
    def get(self):
                template = JINJA_ENVIRONMENT.get_template('index.html')
                self.response.write(template.render())
		
class checklogin(webapp2.RequestHandler):
    def get(self):
        data=[]
        obj=[]
        data = json.loads(cgi.escape(self.request.get('jsonData')))
        t1=User.query(User.emailid==data['email']).get()
        if t1 is None :
            obj = {u"status": "UnSuccessful", u"errorcode":0, u"errormessage":"The Email is not Registered"}
        elif(t1.pin==data['pin']):
            obj = {u"status": "Successful", u"errorcode":1, u"errormessage":"The Login Successful"}
        else :
            obj = {u"status": "UnSuccessful", u"errorcode":0, u"errormessage":"Invalid Credentials"}
        ss=json.dumps(obj)
        self.response.headers.add_header('content-type', 'application/json', charset='utf-8')
        self.response.write(ss)

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

class getanswers(webapp2.RequestHandler):
    def get(self):
       vals = json.loads(cgi.escape(self.request.get('jsonData')))
       print(vals)
       logging.error("currentQuestion,submit")
class audioupload(webapp2.RequestHandler):
    def get(self):
       mp3=self.request.get('audio')
       m=audio(mp3=mp3)
       m.put()
       logging.error("audio uploaded")
       self.response.write("blob saved succesfully")

class getsubmitstatus(webapp2.RequestHandler):
    def get(self):
      q= Response.query(Response.q_status=="submitted").get()
      self.response.write(q.submittedans)


class submit(webapp2.RequestHandler):
    def get(self):
        # opening json file sent by the server
        validresponce="false"
        status=""
        errortype=""
        q_status=""
        score=0
        vals = json.loads(cgi.escape(self.request.get('jsonData')))
        currentQuestion =vals['currentQuestion']
        submittedans = vals['submittedans']
        responsetime = vals['responsetime']
         # opening  json file of quizdata
        #logging.error(currentQuestion,submittedans)
        json_data=json.loads(open('quizdata.json').read())
        #print(json_data )
        #logging.error("This is an error message that will show in the console")
        # finding the correct answer and updating the score
        for currentSection in json_data["section"]:
            for currentSubsection in currentSection["subsection"]:
                for q in currentSubsection["questions"]:
                   # print(q["id"])
                    if q["id"]==str(currentQuestion):
                        if submittedans == "skip":
                            validresponce="true"
                            q_status="skipped"
                           # print(q_status)
                        else:
                            for option in q["options"]:
                                string1=option[1:len(option)]
                               # print(string1)
                               # print(submittedans,"submiteddfdf")
                                #logging.error("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
                                if submittedans == string1:
                                    #print("validrespnse")
                                    validresponce="true"
                                    if option[0]== "=":
                                        score=1
                                        #logging.error("This is an error message that will show in the console")

        if validresponce=="true":
            global status
            status="success"
            if q_status!="skipped":
                q_status="submitted"
        else:
            global status
            status="error"
            global errortype
                   # creating json file for error response
        # placing in to the database
        data=Response(currentQuestion=currentQuestion,submittedans=submittedans,responsetime=responsetime,q_status=q_status,q_score=score)
        data.put()
        obj = {u"status":status , u"q_status":q_status, u"validresponce":validresponce, u"qid":currentQuestion}
        ss=json.dumps(obj)
        self.response.headers.add_header('content-type', 'application/json', charset='utf-8')
        self.response.write(ss)


class AutosaveEssay(webapp2.RequestHandler):
    def get(self):
        vals = json.loads(cgi.escape(self.request.get('jsonData')))
        useremailid = vals['useremailid']
        qid = vals['qid']
        ans = vals['ans']
        qshowntime = vals['qshowntime']
        qattemptedtime = vals['qattemptedtime']

        data1 = EssayTypeResponse.query(EssayTypeResponse.useremailid == useremailid,
                                     EssayTypeResponse.qid == qid).get()
        if data1:
            data1.qshowntime=qshowntime
            data1.qattemptedtime=qattemptedtime
            data1.ansText = ans
            data1.status= vals['status']

        else:
            data = EssayTypeResponse(useremailid=useremailid,
                                     qid=qid+"",
                                     qshowntime=qshowntime,
                                     qattemptedtime=qattemptedtime,
                                     ansText = ans,
                                     status= vals['status'])
            data.put()

application = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/index',signpage),
    ('/signup', checkuser),
    ('/checklogin',checklogin),
    ('/submitanswer', submit),
    ('/getanswers', getanswers),
    ('/audioupload', audioupload),
    ('/getsubmitstatus', getsubmitstatus),
    ('/autosaveEssay', AutosaveEssay),
       ], debug=True)