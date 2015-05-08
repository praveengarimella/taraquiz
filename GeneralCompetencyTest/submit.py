import os
import cgi
import traceback
import json
import jinja2
import webapp2
import logging
from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.ext.webapp import util

from google.appengine.ext import ndb
from google.appengine.api import users
from google.appengine.api import mail
from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.api import files
from pprint import pprint
import datetime
from datetime import datetime
from random import shuffle


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)
def getAllQuestions():
    json_temp=json.loads(open('QuestionBank_template.json').read())
    for key in json_temp:
        if  key == "section":
            section=json_temp[key]
            for s in section:
                for key in s:
                    if key == "subsection":
                        for subs in s[key]:
                            name=subs["name"]
                            types=subs["types"]
                            #print name
                            if name == "E2-Listening":
                                #print name
                                json_subs=json.loads(open(name+".json").read())
                                video_list=json_subs["videoArray"]
                                subs["videoArray"]=video_list
                            if types =="question" or types =="record":
                                #print name
                                json_subs=json.loads(open(name+".json").read())
                                qns_list=json_subs["questions"];
                                subs["questions"]=qns_list
                            if types == "passage":
                                #print name
                                json_subs=json.loads(open(name+".json").read())
                                psglist=json_subs["passageArray"]
                                subs["passageArray"]=psglist
                            if types =="essay":
                                #print name
                                json_subs=json.loads(open(name+".json").read())
                                qns_list=json_subs["questions"];
                                subs["questions"]=qns_list
                            if name == "T2-Listening":
                                #print name
                                json_subs=json.loads(open(name+".json").read())
                                video_list=json_subs["videoArray"]
                                subs["videoArray"]=video_list
    #ss=json.dumps(json_temp)
    return json_temp

def getAnswer(qid):
    qid=int(qid)
    if qid in range(101,201):
        a1_sentjson=json.loads(open('A1-Sentences.json').read())
        for key in a1_sentjson["questions"]:
            if int(key["id"]) == qid:
                for op in key["options"]:
                    if op[0] == "=":
                        return op[1:len(op)]
    if qid in range(201,301):
        a2_readjson=json.loads(open('A2-Reading.json').read())
        for key in a2_readjson["passageArray"]:
            for psg in key["questions"]:
                if int(psg["id"]) == qid:
                    for op in psg["options"]:
                        if op[0] == "=":
                            return op[1:len(op)]
    if qid in range(301,401):
        a3_numjson=json.loads(open('A3-Numerical.json').read())
        for key in a3_numjson["questions"]:
            if int(key["id"]) == qid:
                for op in key["options"]:
                    if op[0] == "=":
                        return op[1:len(op)]
    if qid in range(401,501):
        a4_reasjson=json.loads(open('A4-Reasoning.json').read())
        for key in a4_reasjson["questions"]:
            if int(key["id"]) == qid:
                for op in key["options"]:
                    if op[0] == "=":
                        return op[1:len(op)]

    if qid in range(601,701):
        e1_readjson=json.loads(open('E1-Reading.json').read())
        for psg in e1_readjson["passageArray"]:
            for key in psg["questions"]:
                if int(key["id"]) == qid:
                    for op in key["options"]:
                        if op[0] == "=":
                            return op[1:len(op)]
    if qid in range(701,801):
        e2_lsnjson=json.loads(open('E2-Listening.json').read())
        for key in e2_lsnjson["videoArray"]:
            for qn in key["questions"]:
                if int(qn["id"]) == qid:
                    for op in qn["options"]:
                        if op[0] == "=":
                            return op[1:len(op)]
    if qid in range(1001,1101):
        t1_readjson=json.loads(open('T1-Reading.json').read())
        for key in t1_readjson["passageArray"]:
            for qn in key["questions"]:
                if int(qn["id"]) == qid:
                    for op in qn["options"]:
                        if op[0] == "=":
                            return op[1:len(op)]
    if qid in range(1101,1201):
        t2_lsnjson=json.loads(open('T2-Listening.json').read())
        for key in t2_lsnjson["videoArray"]:
            for qn in key["questions"]:
                if int(qn["id"]) == qid:
                    for op in qn["options"]:
                        if op[0] == "=":
                            return op[1:len(op)]
def getQuestionPaper(qid_list):
    json_temp=json.loads(open('QP_template.json').read())
    #print qid_list
    i=0;j=0;k=0;l=0;m=0;n=0;p=0;q=0;r=0;s=0;t=0
    for qid in qid_list:
        qid=int(qid)
        if qid in range(101,201):
              a1_sentjson=json.loads(open('A1-Sentences.json').read())
              for key in a1_sentjson["questions"]:
                    
                    if int(key["id"]) == qid:
                          #print key
                          json_temp["section"][0]["subsection"][0]["questions"].append(key)
                          json_temp["section"][0]["subsection"][0]["questions"][i]["serialno"]=i+1
                          i +=1
        if qid in range(201,301):
              a2_readjson=json.loads(open('A2-Reading.json').read())
              for key in a2_readjson["passageArray"]:
                    pid=key["questions"][0]["id"]
                    if int(pid) == qid:
                          json_temp["section"][0]["subsection"][1]["passage"]=key["passage"]
                          json_temp["section"][0]["subsection"][1]["questions"]=key["questions"]
                          json_temp["section"][0]["subsection"][1]["questions"][0]["serialno"]=1
        if qid in range(301,401):
              a3_numjson=json.loads(open('A3-Numerical.json').read())
              for key in a3_numjson["questions"]:
                    if int(key["id"]) == qid:
                          json_temp["section"][0]["subsection"][2]["questions"].append(key)
                          json_temp["section"][0]["subsection"][2]["questions"][j]["serialno"]=j+1
                          j +=1
        if qid in range(401,501):
              a4_reasjson=json.loads(open('A4-Reasoning.json').read())
              for key in a4_reasjson["questions"]:
                    if int(key["id"]) == qid:
                          json_temp["section"][0]["subsection"][3]["questions"].append(key)
                          json_temp["section"][0]["subsection"][3]["questions"][k]["serialno"]=k+1
                          k +=1
        if qid in range(501,601):
              a5_essayjson=json.loads(open('A5-Composition.json').read())
              for key in a5_essayjson["questions"]:
                    if int(key["id"]) == qid:
                          json_temp["section"][0]["subsection"][4]["questions"].append(key)
                          json_temp["section"][0]["subsection"][4]["questions"][l]["serialno"]=l+1
                          l += 1
        if qid in range(601,701):
              e1_readjson=json.loads(open('E1-Reading.json').read())
              for key in e1_readjson["passageArray"]:
                    for qn in key["questions"]:
                          pid=qn["id"]
                          if int(pid) == qid:
                                json_temp["section"][1]["subsection"][0]["passage"]=key["passage"]
                                json_temp["section"][1]["subsection"][0]["questions"].append(qn)
                                json_temp["section"][1]["subsection"][0]["questions"][m]["serialno"]=m+1
                                m +=1
        if qid in range(701,801):
              e2_lsnjson=json.loads(open('E2-Listening.json').read())
              for key in e2_lsnjson["videoArray"]:
                    for qn in key["questions"]:
                          pid=qn["id"]
                          if int(pid) == qid:
                                json_temp["section"][1]["subsection"][1]["link"]=key["link"]
                                json_temp["section"][1]["subsection"][1]["questions"].append(qn)
                                json_temp["section"][1]["subsection"][1]["questions"][n]["serialno"]=n+1
                                n +=1
        if qid in range(801,901):
              e3_spkjson=json.loads(open('E3-Speaking.json').read())
              for key in e3_spkjson["questions"]:
                    if int(key["id"]) == qid:
                          json_temp["section"][1]["subsection"][2]["questions"].append(key)
                          json_temp["section"][1]["subsection"][2]["questions"][p]["serialno"]=p+1
                          p += 1
        if qid in range(901,1001):
              e4_wrtjson=json.loads(open('E4-Writing.json').read())
              for key in e4_wrtjson["questions"]:
                    if int(key["id"]) == qid:
                          json_temp["section"][1]["subsection"][3]["questions"].append(key)
                          json_temp["section"][1]["subsection"][3]["questions"][q]["serialno"]=q+1
                          q += 1
        if qid in range(1001,1101):
              t1_readjson=json.loads(open('T1-Reading.json').read())
              for key in t1_readjson["passageArray"]:
                    for qn in key["questions"]:
                          pid=qn["id"]
                          if int(pid) == qid:
                                json_temp["section"][2]["subsection"][0]["passage"]=key["passage"]
                                json_temp["section"][2]["subsection"][0]["questions"].append(qn)
                                json_temp["section"][2]["subsection"][0]["questions"][r]["serialno"]=r+1
                                r += 1
        if qid in range(1101,1201):
              t2_lsnjson=json.loads(open('T2-Listening.json').read())
              for key in t2_lsnjson["videoArray"]:
                    for qn in key["questions"]:
                          pid=qn["id"]
                          if int(pid) == qid:
                                json_temp["section"][2]["subsection"][1]["link"]=key["link"]
                                json_temp["section"][2]["subsection"][1]["questions"].append(qn)
                                json_temp["section"][2]["subsection"][1]["questions"][s]["serialno"]=s+1
                                s += 1
    #ss=json.dumps(json_temp)
    return json_temp
def generateQuestionPaper():
    json_temp=json.loads(open('QP_template.json').read())
    for key in json_temp:
        if  key == "section":
            section=json_temp[key]
            for s in section:
                for key in s:
                    if key == "subsection":
                        for subs in s[key]:
                            cnt=int(subs["count"])
                            name=subs["name"]
                            types=subs["types"]
                            #print name
                            if name == "E2-Listening":
                                #print name
                                json_subs=json.loads(open(name+".json").read())
                                video_list=json_subs["videoArray"]
                                serialno=range(0,len(video_list))
                                shuffle(serialno)
                                subs["link"]=video_list[serialno[0]]["link"]
                                subs["questions"]=video_list[serialno[0]]["questions"]
                                i=0
                                for qn in subs["questions"]:
                                    subs["questions"][i]["serialno"]=i+1
                                    i +=1
                            if types =="question" or types =="record":
                                #print name
                                json_subs=json.loads(open(name+".json").read())
                                qns_list=json_subs["questions"];
                                serialno=range(0,len(qns_list))
                                shuffle(serialno)
                                for no in range(0,cnt):
                                    subs["questions"].append(qns_list[serialno[no]])
                                    subs["questions"][no]["serialno"]=no+1
                            if types == "passage":
                                #print name
                                json_subs=json.loads(open(name+".json").read())
                                psglist=json_subs["passageArray"]
                                serialno=range(0,len(psglist))
                                shuffle(serialno)
                                subs["questions"]=psglist[serialno[0]]["questions"]
                                j=0
                                for qn in subs["questions"]:
                                    subs["questions"][j]["serialno"]=j+1
                                    j +=1
                                subs["passage"]=psglist[serialno[0]]["passage"]
                            if types =="essay":
                                #print name
                                json_subs=json.loads(open(name+".json").read())
                                qns_list=json_subs["questions"];
                                serialno=range(0,len(qns_list))
                                shuffle(serialno)
                                for no in range(0,cnt):
                                    subs["questions"].append(qns_list[serialno[no]])
                                    subs["questions"][no]["serialno"]=no+1
                            if name == "T2-Listening":
                                #print name
                                json_subs=json.loads(open(name+".json").read())
                                video_list=json_subs["videoArray"]
                                serialno=range(0,len(video_list))
                                shuffle(serialno)
                                subs["link"]=video_list[serialno[0]]["link"]
                                subs["questions"]=video_list[serialno[0]]["questions"]
                                k=0
                                for qn in subs["questions"]:
                                  subs["questions"][k]["serialno"]=k+1
                                  k +=1
    #ss=json.dumps(json_temp)
    return json_temp
class UserAudio(ndb.Model):
    user = ndb.StringProperty(indexed=True)
    # blob_key = blobstore.BlobReferenceProperty()
    blob1 = ndb.BlobKeyProperty(indexed=True)
    time=ndb.DateTimeProperty(auto_now_add=True)
class DataModel(db.Model):
	url = db.StringProperty(required=True)
	blob = blobstore.BlobReferenceProperty(required=True)

class User(ndb.Model):
    """Sub model for storing user activity."""
    name = ndb.StringProperty(indexed=True)
    emailid = ndb.StringProperty(indexed=True)
    pin = ndb.StringProperty(indexed=True)
    testctime=ndb.DateTimeProperty(auto_now=True)

class userDetails(ndb.Model):
    name = ndb.StringProperty(indexed=True)    
    email=ndb.StringProperty(indexed=True)
    phno = ndb.StringProperty(indexed=True)
    street = ndb.StringProperty(indexed=True)
    city = ndb.StringProperty(indexed=True)
    state = ndb.StringProperty(indexed=True)
    pincode = ndb.StringProperty(indexed=True)

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
            sp=userDetails.query(userDetails.email==user.email()).get()
            template=None
            print sp
            logging.error("checkllajn")
            if sp is not None:
                template= JINJA_ENVIRONMENT.get_template('quiz.html')
            else:
                template= JINJA_ENVIRONMENT.get_template('register.html')
            self.response.write(template.render())


class getquizstatus(webapp2.RequestHandler):
    """ handling status of quiz sends a json file of responses"""
    def post(self):
        user = users.get_current_user()
        if user:
            #qbank=QuestionBank()
            # check if candidate is resuming the test
            r1 = Randomize.query(Randomize.user1==user.email()).fetch()
            print r1
            logging.error("random values")
            if r1:
                isRandomized = True
                qid_list=[]
                for data in r1:
                    qid_list.append(data.qno);
                json_data=getQuestionPaper(qid_list)
            else:
                isRandomized = False
                json_data=generateQuestionPaper()
            # TODO
            # New json_data returned from the question bank if is randomized is false
            # Else list of question ID should be fetched from randomize table
            # pass the question IDs list to the question bank to get json_data

            #json_data = json.loads(open('quizdata.json').read())
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
                                                if not isRandomized:
                                                    r = Randomize(user1 = user.email(), serialno = q['serialno'], qno=q["id"])
                                                    r.put()
                                                else:
                                                    #print q['id']
                                                    #logging.error("question id is:")
                                                    r = Randomize.query(Randomize.user1 == user.email(),
                                                                        Randomize.qno == q["id"]).get()
                                                q1 = Response.query(Response.useremailid.emailid==user.email(),
                                                                    Response.currentQuestion==q["id"]).order(-Response.time).get()
                                                if q1:
                                                    q["responseAnswer"]=q1.submittedans
                                                    q["responseTime"]=q1.responsetime
                                                    q["status"]=q1.q_status

            td = TestDetails.query(TestDetails.email==user.email()).get()
            if td:
                if td.testend:
                    json_data['quizStatus'] = 'END'
                else:
                    json_data['quizStatus'] = 'INPROGRESS'
            else:
                json_data['quizStatus'] = 'START'

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
                currentQuestion=int(currentQuestion)
                if submittedans == "skip":
                    validresponse="true"
                    q_status="skip"
                elif currentQuestion in range(501,601):
                    q_status="submitted"
                    status="success"
                    validresponse="true"
                elif currentQuestion in range(801,901):
                    r=UserAudio.query(UserAudio.user==user.email()).get()
                    if r :
                        q_status="submitted"
                        status="success"
                        validresponse="true"
                    else :
                        q_status="unknown"
                        status="error with record"
                        validresponse="false"
                elif currentQuestion in range(901,1001):
                    q_status="submitted"
                    status="success"
                    validresponse="true"
                else :
                    q_status="submitted"
                    status="success"
                    validresponse="true"
                    cans=getAnswer(currentQuestion)
                    if cans == submittedans:
                        score = 1
                if validresponse=="true":
                    global status
                    status="success"
                    if q_status!="skip":
                        q_status="submitted"
                else:
                    global status
                    status="error"
                    global errortype
                # json_data=json.loads(open('quizdata.json').read())

                # # finding the correct answer and updating the score
                # for currentSection in json_data["section"]:
                #     for currentSubsection in currentSection["subsection"]:
                #         type=currentSubsection["types"]
                #         #logging.error("This is an error message that will show in the console")
                #         print type
                #         for q in currentSubsection["questions"]:
                #             # print(q["id"])
                #             if q["id"]==str(currentQuestion):
                #                 if submittedans == "skip":
                #                     validresponse="true"
                #                     q_status="skip"
                #                     # print(q_status)
                #                 else:
                #                     type=currentSubsection["types"]
                #                     if type=="essay":
                #                         q_status="submitted"
                #                         status="success"
                #                         validresponse="true"
                #                     elif type=="record":
                #                         r=UserAudio.query(UserAudio.user==user.email()).get()
                #                         if r :
                #                             q_status="submitted"
                #                             status="success"
                #                             validresponse="true"
                #                         else :
                #                             q_status="unknown"
                #                             status="error with record"
                #                             validresponse="false"
                #                     else :
                #                         for option in q["options"]:
                #                             string1=option[1:len(option)]
                #                             # print(string1)
                #                             # print(submittedans,"submiteddfdf")
                #                             #logging.error("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
                #                             if submittedans == string1:
                #                                 #print("validrespnse")
                #                                 validresponse="true"
                #                                 if option[0]== "=":
                #                                     score=1
                #                                     #logging.error("This is an error message that will show in the console")

                # if validresponse=="true":
                #     global status
                #     status="success"
                #     if q_status!="skip":
                #         q_status="submitted"
                # else:
                #     global status
                #     status="error"
                #     global errortype


                # creating json file for error response
                # placing in to the database
                n1=int(currentQuestion)
                data=Response(serialno=n1,useremailid=User(emailid=user.email(),name=user.nickname()),currentQuestion=str(currentQuestion),submittedans=submittedans,responsetime=responsetime,q_status=q_status,q_score=score)
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
            duration = 70 * 60
            td = TestDetails.query(TestDetails.email==user.email()).get()
            if td is None:
                TestDetails(email=user.email(),test=True,delays=0.0).put()
                obj = {u"timeSpent":0, u"timeRemaining":duration, u"quizStatus": u"INPROGRESS"}
            else:
                if not td.testend:
                    currTime = datetime.now()
                    deltaTime = (currTime - td.lastPing).total_seconds()
                    if(deltaTime > 65.0):
                        td.delays = td.delays + deltaTime - 60.0
                        td.put()
                    timeSpent = (currTime - td.teststime).total_seconds() - td.delays

                    if timeSpent >= duration:
                        td.testend = True
                        quizStatus = u"END"
                    else:
                        quizStatus = u"INPROGRESS"
                    obj = {u"timeSpent" : timeSpent, u"quizStatus": quizStatus, u"timeRemaining" : duration - timeSpent}
                    td.lastPing = currTime
                    td.put()
                else:
                    obj = {u"quizStatus":u"END"}
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

class registrationdataHandler(webapp2.RequestHandler):
    def post(self):
        user = users.get_current_user()
        if user:
            vals = json.loads(cgi.escape(self.request.body))
            vals = vals['jsonData']
            userDetails(name=vals['name'],email=user.email(),phno=vals['phno'],street=vals['add1'],city=vals['add2'],state=vals['add3'],pincode=vals['pincode']).put()
            obj = {u"message": "success"}
            ss=json.dumps(vals)
            self.response.headers.add_header('content-type', 'application/json', charset='utf-8')
            self.response.write(ss)
        else:
            login_url = users.create_login_url(self.request.path)
            self.redirect(login_url)

    def get(self):
        user=users.get_current_user()
        if user:
            template = JINJA_ENVIRONMENT.get_template('quiz.html')
            self.response.write(template.render())
        else:
            login_url = users.create_login_url(self.request.path)
            self.redirect(login_url)

class registration(webapp2.RequestHandler):
    def get(self):
        user=users.get_current_user()
        if user:
            template = JINJA_ENVIRONMENT.get_template('register.html')
            self.response.write(template.render())
        else:
            login_url = users.create_login_url(self.request.path)
            self.redirect(login_url)
			
class WamiHandler(webapp2.RequestHandler):
    def post(self):
        user= users.get_current_user()
        if user:
            type = self.request.headers['Content-Type']
            blob_file_name = files.blobstore.create(mime_type=type, _blobinfo_uploaded_filename=self.get_name())
            with files.open(blob_file_name, 'a') as f:
                f.write(self.request.body)
            f.close()
            files.finalize(blob_file_name)
            blob_key = files.blobstore.get_blob_key(blob_file_name)
            UserAudio(blob1=blob_key,user=user.email()).put()
            logging.info("client-to-server: type(" + type +") key("  + str(blob_key) + ")")
			
		
    def get_name(self):
        name = "output.wav"
        params = cgi.parse_qs(self.request.query_string)
        if params and params['name']:
            name = params['name'][0];
        return name
            
class endtest(webapp2.RequestHandler):
    def post(self):
        user = users.get_current_user()
        if user:
            val = json.loads(cgi.escape(self.request.body))
            val = val['jsonData']
            testend = val['testend']
            print(testend)
            data1 = TestDetails.query(TestDetails.email == user.email()).get()
            print(user.email())      
            if data1:
                data1.testend = testend
                data1.put()

application = webapp2.WSGIApplication([
    ('/', homepage),
    ('/checklogin',checklogin),
    ('/startquiz',registrationdataHandler),
    ('/registration',registration),
    ('/submitanswer', submitAnswer),
    ('/getResult', getResult),
    ('/getquizstatus', getquizstatus),
    ('/getScore', getScore),
    ('/autosaveEssay', AutosaveEssay),
    ('/uploadredirect',UploadRedirect),
    ('/upload_audio', AudioUploadHandler),
    ('/view_audio/([^/]+)?', ViewAudioHandler),
    ('/testtime',storetime),
	('/audio',WamiHandler),
    ('/endtest',endtest)
], debug=True)