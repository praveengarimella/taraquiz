import json
from random import shuffle
class Questionbank(object):
    def __init__(self):
        pass
    def getAllQuestions(self):
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
        ss=json.dumps(json_temp)
        return ss

    def getAnswer(self,qid):
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
    def getQuestionPaper(self,qid_list):
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
        ss=json.dumps(json_temp)
        return ss
    def generateQuestionPaper(self):
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
        ss=json.dumps(json_temp)
        return ss
# q=Questionbank()
# qid_list=[306,110,604,603,115,708,106,116,126,201,706,707,330,310,303,412,404,510,601,602,705,811,911,1001,1002,1003,1004,1101,1102,1103]
# final_data=q.getQuestionPaper(qid_list)
# #final_data=q.generateQuestionPaper()
# #ans=q.getAnswer(1102)
# #ss=json.dumps(ans)
# #print ss
# #data=q.getAllQuestions()
# print final_data

