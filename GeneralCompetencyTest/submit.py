import os
import cgi
from google.appengine.ext import ndb
from google.appengine.api import users
from google.appengine.api import mail
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
    serialno=ndb.IntegerProperty(indexed=True)

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
       
class homepage(webapp2.RequestHandler):
    """  handles rendering of index page """
    def get(self):
                template = JINJA_ENVIRONMENT.get_template('index.html')
                self.response.write(template.render())
		
class checklogin(webapp2.RequestHandler):
    """ handles authentication and redirects to quiz page """
    def get(self):
	user = users.get_current_user()
        if user is None:
          login_url = users.create_login_url(self.request.path)
          self.redirect(login_url)
          return
	else:
	    Response(useremailid=User(emailid=user.email(),name=user.nickname())).put()
	    template= JINJA_ENVIRONMENT.get_template('quiz.html')
            self.response.write(template.render())


class getquizstatus(webapp2.RequestHandler):
    """ handling status of quiz sends a json file of responses"""
    def get(self):
      user = users.get_current_user()
      if user:
        q1 = Response.query(Response.useremailid.emailid==user.email(),Response.currentQuestion!=None).get()
        json_data=json.loads(open('quizdata.json').read())
        print json_data["name"]
        logging.error("This is an error message that will show in the console")
        print "hello"
        if q1:
          for key in json_data:
              if  key == "section":
                  section = json_data[key]
                  for s in  section:
                      for key in s:
                          if key == "subsection":
                              for subs in s[key]:
                                  for key in subs:
                                      if key == "questions":
                                          for q in subs[key]:
                                             q1 = Response.query(Response.currentQuestion==q["id"]).order(-Response.time).get()
                                             if q1:
                                              q["responseAnswer"]=q1.submittedans
                                              q["responseTime"]=q1.responsetime
                                              q["status"]=q1.q_status

        ss=json.dumps(json_data)
        self.response.headers.add_header('content-type', 'application/json', charset='utf-8')
        self.response.write(ss)

class getResult(webapp2.RequestHandler):
    """ get result for entire quiz """
    def get(self):
        totalscore=0
        user = users.get_current_user()
        if user is None:
          login_url = users.create_login_url(self.request.path)
          self.redirect(login_url)
          return
        else:
          q1= Response.query(Response.useremailid.emailid==user.email())
          q1=q1.order(Response.serialno,-Response.time)
          questionresponses_dict = {}
          question_records=[]
          totalscore=0
          s1="0"
          for q in q1:
            if q.responsetime is not None:
                if q.currentQuestion != s1 :
                  s1=q.currentQuestion
                  #totalscore=q.responsetime+q.q_score
                  question = {"user":user.nickname(),"submittedans":q.submittedans, "q_score":q.currentQuestion,"currentQuestion":s1,"responsetime":q.responsetime}
                  question_records.append(question)
          questionresponses_dict["question"]=question_records
          questionresponses_dict["totalscore"]=totalscore
          ss=json.dumps(questionresponses_dict)
          self.response.headers.add_header('content-type', 'application/json', charset='utf-8')
          self.response.write(ss)

class getScore(webapp2.RequestHandler):
    """ get score for entire quiz """
    def get(self):
        score=0
        user = users.get_current_user()
        if user is None:
          login_url = users.create_login_url(self.request.path)
          self.redirect(login_url)
          return
        else:
          q1= Response.query(Response.useremailid.emailid==user.email())
          q1.fetch()
          q1= Response.query(Response.useremailid.emailid==user.email())
          q1.fetch()
          for q in q1:
            score=score+1
          template_values = {
                'p': q1,
                'score1':score,
                }
          template = JINJA_ENVIRONMENT.get_template('testresult.html')
          self.response.write(template.render(template_values))    

class submitAnswer(webapp2.RequestHandler):
    """ submting question response , sends a json file of response"""
    def get(self):
        user = users.get_current_user()
        if user is None:
          login_url = users.create_login_url(self.request.path)
          self.redirect(login_url)
          return
        else:
            # opening json file sent by the server
            validresponce="false"
            status=""
            errortype=""
            q_status=""
            score=0
            vals = json.loads(cgi.escape(self.request.get('jsonData')))
            logging.error("testing json values");
            print vals
            currentQuestion =vals['id']
            submittedans = vals['responseAnswer']
            responsetime = vals['responseTime']
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
                            if submittedans == "Skip":
                                validresponce="true"
                                q_status="skip"
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
                if q_status!="skip":
                    q_status="submitted"
            else:
                global status
                status="error"
                global errortype
            # creating json file for error response
            # placing in to the database
            n1=int(currentQuestion)
            data=Response(serialno=n1,useremailid=User(emailid=user.email(),name=user.nickname()),currentQuestion=currentQuestion,submittedans=submittedans,responsetime=responsetime,q_status=q_status,q_score=score)
            data.put()
            obj = {u"status":status , u"q_status":q_status, u"validresponce":validresponce, u"qid":currentQuestion}
            ss=json.dumps(obj)
            self.response.headers.add_header('content-type', 'application/json', charset='utf-8')
            self.response.write(ss)

class AutosaveEssay(webapp2.RequestHandler):
    """ saving essay writing response"""
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
    ('/', homepage),
    ('/checklogin',checklogin),
    ('/submitanswer', submitAnswer),
    ('/getResult', getResult),
    ('/getquizstatus', getquizstatus),
    ('/getScore', getScore),
    ('/autosaveEssay', AutosaveEssay),  
       ], debug=True)