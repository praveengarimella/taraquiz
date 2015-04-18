import os
import cgi
import traceback
import json
import jinja2
import webapp2
import logging
from google.appengine.ext import ndb
from google.appengine.api import users
from google.appengine.api import mail
from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers
from google.appengine.ext.webapp.util import run_wsgi_app
from pprint import pprint
import datetime
from datetime import datetime
from random import shuffle


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)
class UserAudio(ndb.Model):
    user = ndb.StringProperty()
    # blob_key = blobstore.BlobReferenceProperty()
    blob_key = ndb.BlobKeyProperty()
class User(ndb.Model):
    """Sub model for storing user activity."""
    name = ndb.StringProperty(indexed=True)
    emailid = ndb.StringProperty(indexed=True)
    pin = ndb.StringProperty(indexed=True)
    testctime=ndb.DateTimeProperty(auto_now=True)

class TestDetails(ndb.Model):
    email=ndb.StringProperty(indexed=True)
    test= ndb.BooleanProperty(default=False)
    teststime=ndb.DateTimeProperty(auto_now_add=True)
    delays=ndb.FloatProperty(indexed=True)
    testend= ndb.BooleanProperty(default=False)
    lastPing = ndb.DateTimeProperty(auto_now_add=True)

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

class Randomize(ndb.Model):
    user1=ndb.StringProperty(indexed = True)
    serialno=ndb.IntegerProperty(indexed= True)
    qno=ndb.StringProperty(indexed = True)

class EssayTypeResponse(ndb.Model):
    """Sub model for storing user response for essay type questions"""
    useremailid = ndb.StringProperty(indexed = True)
    qid = ndb.StringProperty(indexed = True)
    ansText = ndb.StringProperty(indexed = True)
    qattemptedtime = ndb.FloatProperty(indexed = True)

class UploadRedirect(webapp2.RequestHandler):
    def post(self):
        upload_url=blobstore.create_upload_url('/upload_audio');
        self.response.write(upload_url)
        #self.redirect("/upload_audio")
class AudioUploadHandler(blobstore_handlers.BlobstoreUploadHandler):
    def post(self):
        try:
            #filename=self.request.get("audio-blob");
            #blobstore_key=blobstore.create_gs_key(filename)
            #blobkey=blobstore.BlobKey(blobstore_key)
            user = users.get_current_user()
            if user:
                upload = self.get_uploads()[0]
                #uname=str(users.get_current_user().email())
                user_audio = UserAudio(user=user.email(), blob_key=upload.key())
                user_audio.put()
                #print str(filename)
                #logging.error("upload value")
                # self.redirect('/view_audio/%s' % upload.key())
                #self.response.write("Uploaded success")
        except Exception,e:
            traceback.print_exc()
            logging.error("error occured.."+str(e))
            self.response.write("Record not saved")
# [END audio_handler]

# [START download_handler]
class ViewAudioHandler(blobstore_handlers.BlobstoreDownloadHandler):
    def get(self, audio_key):
        if not blobstore.get(photo_key):
            self.error(404)
        else:
            resource = str(urllib.unquote(audio_key))
            blob_info = blobstore.BlobInfo.get(resource)
            self.send_blob(blob_info,save_as=True)
            self.response.write(str(key))
# # [END download_handler]    
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
            ss=Response.query(Response.useremailid.emailid==user.email()).get()
            if ss is None:
                Response(useremailid=User(emailid=user.email(),name=user.nickname())).put()
            template= JINJA_ENVIRONMENT.get_template('quiz.html')
            self.response.write(template.render())


class getquizstatus(webapp2.RequestHandler):
    """ handling status of quiz sends a json file of responses"""
    def post(self):
        user = users.get_current_user()
        if user:
            #q1 = Response.query(Response.useremailid.emailid==user.email(),Response.currentQuestion!=None).get()
            #print q1
            #logging.error("This is an error message that will show in the console")
            td = TestDetails.query(TestDetails.email==user.email()).get()
            json_data=json.loads(open('1quizdata.json').read())
            r1 = Randomize.query(Randomize.user1==user.email()).get()
            logging.error("examine random result set")
            if r1:
                isRandomized = True
            else:
                isRandomized = False
            # if q1:
            for key in json_data:
                if  key == "section":
                    section = json_data[key]
                    for s in  section:
                        for key in s:
                            if key == "subsection":
                                for subs in s[key]:
                                    for key in subs:
                                        if key == "questions":
                                            if not isRandomized:
                                                serialnos = range(0,len(subs[key]))
                                                shuffle(serialnos)
                                            for q in subs[key]:
                                                if not isRandomized:
                                                    sno = serialnos.pop()
                                                    q["serialno"] = sno
                                                    r = Randomize(user1=user.email(),serialno=sno,qno=q["id"])
                                                    r.put()
                                                else:
                                                    r = Randomize.query(Randomize.user1==user.email(),
                                                                        Randomize.qno==q["id"]).get()
                                                    q["serialno"] = r.serialno

                                                q1 = Response.query(Response.useremailid.emailid==user.email(),
                                                                    Response.currentQuestion==q["id"]).order(-Response.time).get()
                                                if q1:
                                                    q["responseAnswer"]=q1.submittedans
                                                    q["responseTime"]=q1.responsetime
                                                    q["status"]=q1.q_status
            if td:
                json_data['testEnd'] = td.testend

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
                        question = {"user":user.nickname(),"submittedans":q.submittedans, "q_score":q.q_score,"currentQuestion":s1,"responsetime":q.responsetime}
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
    def post(self):
        user = users.get_current_user()
        if user is None:
            login_url = users.create_login_url(self.request.path)
            self.redirect(login_url)
            return
        else:
            # quiz timer code starts here
            # this part will check the delay and compute the time taken
            td=TestDetails.query(TestDetails.email==user.email()).get()
            if td and not td.testend:
                validresponse="false"
                status=""
                errortype=""
                q_status=""
                score=0
                type=""
                logging.error("printing json values");
                vals = json.loads(cgi.escape(self.request.body))
                vals = vals['jsonData']
                currentQuestion =vals['id']
                submittedans = vals['responseAnswer']
                responsetime = vals['responseTime']
                # opening  json file of quizdata
                #logging.error(currentQuestion,submittedans)
                json_data=json.loads(open('quizdata.json').read())

                # finding the correct answer and updating the score
                for currentSection in json_data["section"]:
                    for currentSubsection in currentSection["subsection"]:
                        type=currentSubsection["types"]
                        #logging.error("This is an error message that will show in the console")
                        print type
                        for q in currentSubsection["questions"]:
                            # print(q["id"])
                            if q["id"]==str(currentQuestion):
                                if submittedans == "skip":
                                    validresponse="true"
                                    q_status="skip"
                                    # print(q_status)
                                else:
                                    type=currentSubsection["types"]
                                    if type=="essay":
                                        q_status="submitted"
                                        status="success"
                                        validresponse="true"
                                    elif type=="record":
                                        r=UserAudio.query(UserAudio.user==user.email()).get()
                                        if r :
                                            q_status="submitted"
                                            status="success"
                                            validresponse="true"
                                        else :
                                            q_status="unknown"
                                            status="error with record"
                                            validresponse="false"
                                    else :
                                        for option in q["options"]:
                                            string1=option[1:len(option)]
                                            # print(string1)
                                            # print(submittedans,"submiteddfdf")
                                            #logging.error("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
                                            if submittedans == string1:
                                                #print("validrespnse")
                                                validresponse="true"
                                                if option[0]== "=":
                                                    score=1
                                                    #logging.error("This is an error message that will show in the console")

                if validresponse=="true":
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

                # added time taken based on the timer
                obj = {u"status":status , u"q_status":q_status, u"validresponse":validresponse, u"qid":currentQuestion}

            else:
                obj = {u"testEnd" : True}
            ss=json.dumps(obj)
            self.response.headers.add_header('content-type', 'application/json', charset='utf-8')
            self.response.write(ss)

# this class is to get the ping requests every minute
class storetime(webapp2.RequestHandler):
    def post(self):
        user = users.get_current_user()
        # todo handle user is None by forwarding to sign in?
        if user:
            duration = 60 * 60
            td = TestDetails.query(TestDetails.email==user.email()).get()
            if td is None:
                TestDetails(email=user.email(),test=True,delays=0.0).put()
                obj = {u"timeSpent":0, u"timeRemaining":duration}
            else:
                if not td.testend:
                    currTime = datetime.now()
                    deltaTime = (currTime - td.lastPing).total_seconds()
                    if(deltaTime > 65.0):
                        td.delays = td.delays + deltaTime - 60.0
                        td.put()
                    timeSpent = (currTime - td.teststime).total_seconds() - td.delays

                    if timeSpent >= duration:
                        td.testend = True;
                    obj = {u"timeSpent" : timeSpent, u"testEnd" : td.testend, u"timeRemaining" : duration - timeSpent}
                    td.lastPing = currTime
                    td.put()
                else:
                    obj = {u"testEnd":td.testend}
            ss=json.dumps(obj)
            self.response.headers.add_header('content-type', 'application/json', charset='utf-8')
            self.response.write(ss)

class AutosaveEssay(webapp2.RequestHandler):
    """ saving essay writing response"""
    def post(self):
        user = users.get_current_user()
        vals = json.loads(cgi.escape(self.request.body))
        vals = vals['jsonData']
        qid = vals['currentQuestion']
        ans = vals['draft']
        qattemptedtime = vals['responsetime']
        print(vals)
        logging.error("This is an error message that will show in the console")
        data1 = EssayTypeResponse.query(EssayTypeResponse.useremailid == user.email(),
                                        EssayTypeResponse.qid == qid).get()
        print(user.email())
        print(qid)

        if data1:
            data1.qattemptedtime=qattemptedtime
            data1.ansText = ans
            data1.put()

        else:
            data = EssayTypeResponse(useremailid=user.email(),
                                     qid=qid,
                                     qattemptedtime=qattemptedtime,
                                     ansText = ans,
                                     )
            data.put()

        ss=json.dumps(vals)
        self.response.headers.add_header('content-type', 'application/json', charset='utf-8')
        self.response.write(ss)


application = webapp2.WSGIApplication([
    ('/', homepage),
    ('/checklogin',checklogin),
    ('/submitanswer', submitAnswer),
    ('/getResult', getResult),
    ('/getquizstatus', getquizstatus),
    ('/getScore', getScore),
    ('/autosaveEssay', AutosaveEssay),
    ('/uploadredirect',UploadRedirect),
    ('/upload_audio', AudioUploadHandler),
    ('/view_audio/([^/]+)?', ViewAudioHandler),
    ('/testtime',storetime)
], debug=True)