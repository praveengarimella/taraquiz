import os
import cgi
import traceback
import json
import jinja2
import webapp2
import logging
import csv
from google.appengine.ext import ndb
from google.appengine.api import users
from google.appengine.api import mail
from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers
from google.appengine.ext.webapp.util import run_wsgi_app
from pprint import pprint
from google.appengine.api import mail
from submit import Response,User,TestDetails
import datetime



JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)
ADMIN_USER_IDS=['pg@taramt.com']; 

class RKV(ndb.Model):
    emailid = ndb.StringProperty(indexed=True)
    teststime = ndb.DateTimeProperty(indexed=True)
    testend = ndb.DateTimeProperty(indexed=True)
    aptitude_score = ndb.IntegerProperty(indexed=True)
    english_score = ndb.IntegerProperty(indexed=True)
    telugu_score = ndb.IntegerProperty(indexed=True)

class Invities(ndb.Model):
  """model for storing invited users"""
  emailid=ndb.StringProperty(indexed=True)
  status=ndb.StringProperty(indexed=True)

class RankEntity(ndb.Model):
  emailid=ndb.StringProperty(indexed=True)
  score=ndb.IntegerProperty(indexed=True)
  restime=ndb.IntegerProperty(indexed=True)
  aptitudeScore=ndb.IntegerProperty(indexed=True)
  englishScore=ndb.IntegerProperty(indexed=True)
  teluguScore=ndb.IntegerProperty(indexed=True)
  aptituderestime=ndb.IntegerProperty(indexed=True)
  englishrestime=ndb.IntegerProperty(indexed=True)
  telugurestime=ndb.IntegerProperty(indexed=True)

class checklogin(webapp2.RequestHandler):
    """ handles authentication and redirects to quiz page """
    def get(self):
      user = users.get_current_user()
      if user is None:
        login_url = users.create_login_url(self.request.path)
        self.redirect(login_url)
        return
      else:
        if user.email() in ADMIN_USER_IDS:
          template= JINJA_ENVIRONMENT.get_template('admin.html')
          self.response.write(template.render())
        else:
          Response(useremailid=User(emailid=user.email(),name=user.nickname())).put()
          template= JINJA_ENVIRONMENT.get_template('quiz.html')
          self.response.write(template.render())

class AdminHome(webapp2.RequestHandler):
  def  get(self):
    user = users.get_current_user()
    if user is None:
      login_url = users.create_login_url(self.request.path)
      self.redirect(login_url)
      return
    else:
      if user.email() in ADMIN_USER_IDS:
        userslist={};
        q1= TestDetails.query();
        q1.fetch();
        count=1;
        for data in q1:
          dt=data.teststime;
          dateval=dt.date()
          if not userslist.has_key(dateval):
            count=1;
            userslist[dateval]=count;
          else:
            count +=1;
            userslist[dateval]=count;
        template_values = {'tests':userslist}
        template = JINJA_ENVIRONMENT.get_template('admin.html')
        self.response.write(template.render(template_values))
      else:
        users.create_logout_url('/')
        login_url = users.create_login_url(self.request.path)
        #self.redirect(login_url)
        self.response.write("<center><h3><font color='red'>Invalid Admin Credentials</font></h3><h3>Please <a href='%s'>Login</a> Again</h3></center>"% login_url);
class QuizDetails(webapp2.RequestHandler):
  def  get(self,dateval):
    userslist=[];
    ranklist=[];
    q1= Response.query(ndb.AND(Response.time > datetime.datetime(2015, 4, 20, 6, 00),
                                       Response.time < datetime.datetime(2015, 4, 20, 15, 00))).count();
    print q1
    logging.error("Count of q1 is?")
    #scorecount=0;
    #responseTime=0;
    for data in q1:
      mailid=data.useremailid.emailid;
      udateval=data.time.date();
      if str(udateval) == dateval:
        if mailid not in userslist:
          userslist.append(mailid);
    for users in userslist:
      q2= Response.query(Response.useremailid.emailid==users).order(Response.serialno)
      q2.fetch()
      aptitudescore=0;
      englishtestscore=0;
      telugutestscore=0;
      aptituderestime=0;
      englishrestime=0;
      telugurestime=0;
      scorecount=0;
      responseTime=0;
      counter=0;
      for record in q2:
        if not record.q_score==None:
          if counter<=18:
            aptitudescore +=record.q_score;
            aptituderestime +=record.responsetime;
          elif counter>18 and counter<=27:
            englishtestscore +=record.q_score;
            englishrestime +=record.responsetime;
          elif counter>27 and counter<=34:
            telugutestscore +=record.q_score;
            telugurestime +=record.responsetime;
          scorecount +=record.q_score;
          responseTime +=record.responsetime;
          counter +=1;
      rankent=RankEntity(emailid=users,score=scorecount,restime=int(round(responseTime)),aptitudeScore=aptitudescore,aptituderestime=int(round(aptituderestime)),englishScore=englishtestscore,englishrestime=int(round(englishrestime)),teluguScore=telugutestscore,telugurestime=int(round(telugurestime)))
      ranklist.append(rankent);
    n=len(ranklist);
    for j in range(0,n-1):
      Max=j
      for i in range(j+1,n):
        if(ranklist[i].score>ranklist[Max].score):
          Max=i;
        elif (ranklist[i].score==ranklist[Max].score):
          if(ranklist[i].restime<ranklist[Max].restime):
            Max=i;
      if(not Max==j):
        ranklist[j],ranklist[Max]=ranklist[Max],ranklist[j];
    template_values = {'userslist':ranklist,'dateval':dateval}
    template = JINJA_ENVIRONMENT.get_template('admin.html')
    self.response.write(template.render(template_values))
class UserQuizReport(webapp2.RequestHandler):
  def  get(self,umailid,dateval):
          q1= Response.query(ndb.AND(Response.useremailid.emailid==umailid,Response.serialno!=None)).order(Response.serialno,-Response.time)
          q1.fetch()
          quizdata=[]
          score=0
          for q in q1:
            resp=Response(serialno=q.serialno,useremailid=User(emailid=umailid,name=""),currentQuestion=q.currentQuestion,submittedans=q.submittedans,responsetime=round(q.responsetime),q_status=q.q_status,q_score=q.q_score)
            quizdata.append(resp);
            if not q.q_score==None:
              score += q.q_score;
          json_data=json.loads(open('quizdata.json').read())
            #print(json_data )
            #logging.error("This is an error message that will show in the console")
            # finding the correct answer and updating the score
          questionslist=[];
          correctAnslist=[];
          for currentSection in json_data["section"]:
              for currentSubsection in currentSection["subsection"]:
                    logging.error("This is an error message that will show in the console")
                    for q in currentSubsection["questions"]:
                      questionName=q["question"];
                      questionslist.append(questionName);
                      type=currentSubsection["types"]
                      if (type=="essay" or type=="record"):
                        correctAnslist.append("");
                      else:
                        for option in q["options"]:
                          if option[0]== "=":
                            correctAns=option[1:len(option)];
                            correctAnslist.append(correctAns);
          template_values = {
                'quizdata': quizdata,
                'score':score,
                'questionslist':questionslist,
                'correctAnslist':correctAnslist,
                'useremailid':umailid,
                'dateval':dateval,
                }
          template = JINJA_ENVIRONMENT.get_template('admin.html')
          self.response.write(template.render(template_values))
class DownloadCSV_User(webapp2.RequestHandler):
  def get(self,useremailid):
    self.response.headers['Content-Type'] = 'text/csv'
    self.response.headers['Content-Disposition'] = 'attachment; filename='+useremailid+'_report.csv'
    writer = csv.writer(self.response.out)
    writer.writerow(['Question ID', 'Question','Score','Submitted Answer','Correct Answer','Response time' ])
    json_data=json.loads(open('quizdata.json').read())
    questionslist=[];
    correctAnslist=[];
    for currentSection in json_data["section"]:
      for currentSubsection in currentSection["subsection"]:
        logging.error("This is an error message that will show in the console")
        for q in currentSubsection["questions"]:
          questionName=q["question"];
          questionslist.append(questionName);
          type=currentSubsection["types"]
          if (type=="essay" or type=="record"):
            correctAnslist.append("");
          else:
            for option in q["options"]:
              if option[0]== "=":
                correctAns=option[1:len(option)];
                correctAnslist.append(correctAns);
    q1= Response.query(ndb.AND(Response.useremailid.emailid==useremailid,Response.serialno!=None)).order(Response.serialno,-Response.time)
    q1.fetch()
    score=0
    i=0;
    for q in q1:
      qname=questionslist[i];
      cans=correctAnslist[i];
      restime=round(q.responsetime);
      row=[i+1,qname.encode('utf-8'),q.q_score,q.submittedans.encode('utf-8'),cans.encode('utf-8'),restime]

      writer.writerow(row);
      if not q.q_score==None:
        score += q.q_score;
      i +=1;
class DownloadCSV(webapp2.RequestHandler):
  def get(self,dateval):
    self.response.headers['Content-Type'] = 'text/csv'
    self.response.headers['Content-Disposition'] = 'attachment; filename='+dateval+'_report.csv'
    writer = csv.writer(self.response.out)
    writer.writerow(['UserEmailID', 'Aptitude Score','English Comprehension Score','Telugu Comprehension Score','Total Score','Response time','Rank' ])
    userslist=[];
    ranklist=[];
    q1= Response.query();
    q1.fetch();
    #scorecount=0;
    #responseTime=0;
    for data in q1:
      mailid=data.useremailid.emailid;
      udateval=data.time.date();
      if str(udateval) == dateval:
        if mailid not in userslist:
          userslist.append(mailid);
    for users in userslist:
      q2= Response.query(Response.useremailid.emailid==users).order(Response.serialno)
      q2.fetch()
      aptitudescore=0;
      englishtestscore=0;
      telugutestscore=0;
      scorecount=0;
      responseTime=0;
      counter=0;
      for record in q2:
        if not record.q_score==None:
          if counter<=18:
            aptitudescore +=record.q_score;
          elif counter>18 and counter<=27:
            englishtestscore +=record.q_score;
          elif counter>27 and counter<=34:
            telugutestscore +=record.q_score;
          scorecount +=record.q_score;
          responseTime +=record.responsetime;
          counter +=1;
      rankent=RankEntity(emailid=users,score=scorecount,restime=int(round(responseTime)),aptitudeScore=int(round(aptitudescore)),englishScore=int(round(englishtestscore)),teluguScore=int(round(telugutestscore)))
      ranklist.append(rankent);
    n=len(ranklist);
    for j in range(0,n-1):
      Max=j
      for i in range(j+1,n):
        if(ranklist[i].score>ranklist[Max].score):
          Max=i;
        elif (ranklist[i].score==ranklist[Max].score):
          if(ranklist[i].restime<ranklist[Max].restime):
            Max=i;
      if(not Max==j):
        ranklist[j],ranklist[Max]=ranklist[Max],ranklist[j];
    i=0;
    for q in ranklist:
      row=[q.emailid.encode('utf-8'),q.aptitudeScore,q.englishScore,q.teluguScore,q.score,q.restime,i+1]
      writer.writerow(row);
      i +=1;
class SendInvites(webapp2.RequestHandler):
  def post(self):
    emails=self.request.get("mailids");
    msg=self.request.get("msg");
    message = mail.EmailMessage(sender="narsimha898@gmail.com",
                            subject="Test invitation")
    message.body = msg;
    mailids=emails.split(',');
    for email in mailids:
      message.to = email;
      invities = Invities(emailid=email, status="Invited")
      invities.put()
      message.send()

    self.response.write("<center><h2>The invitations are successfully sent</h2>");
    self.response.write("<center><h2>Click<a href='/admin/'>adminhome</a>to go to adminhome</h2>");
    
class SendInvitesView(webapp2.RequestHandler):
  def get(self):
    template = JINJA_ENVIRONMENT.get_template('sendinvites.html')
    self.response.write(template.render())

class Stats(webapp2.RequestHandler):
    def get(self):
        td = TestDetails.query(ndb.AND(TestDetails.teststime > datetime.datetime(2015, 4, 20, 6, 00),
                                       TestDetails.teststime < datetime.datetime(2015, 4, 20, 15, 00))).count()
        print td
        logging.error("td count fu test")

application = webapp2.WSGIApplication([
    ('/admin/?',AdminHome),
    ('/admin/quizdetails/([^/]+)?',QuizDetails),
    ('/admin/userquizreport/([^/]+)?/([^/]+)?',UserQuizReport), 
    ('/admin/downloadcsv/([^/]+)?',DownloadCSV),
    ('/admin/downloadcsv_user/([^/]+)?',DownloadCSV_User),
    ('/admin/sendinvitesview',SendInvitesView),
    ('/admin/sendinvites',SendInvites),
    ('/admin/stats',Stats),
       ], debug=True)