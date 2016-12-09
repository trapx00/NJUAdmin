from app import app,login,course_table
from bs4 import BeautifulSoup
import json, requests, os, http.cookiejar, datetime
from flask import render_template,request, url_for, g, session, redirect, make_response, send_file


l=lambda : login.login("161250010","162642")
urls = {
    "peCard": "http://mapp.nju.edu.cn/mobile/getExerciseInfo.mo", #start and end time needed startDate=2016-08-29&endDate=2017-01-08
    "termDate": "http://mapp.nju.edu.cn/mobile/getTermDateInfo.mo", #included all term date
    "cardInfo": "http://mapp.nju.edu.cn/mobile/getCardInfo.mo",
    "transInfo":"http://mapp.nju.edu.cn/mobile/getTransList.mo", #pageSize can be provided
    "weeksInfo":"http://mapp.nju.edu.cn/mobile/fetchWeek_qyy.mo", 
    "days":"http://mapp.nju.edu.cn/mobile/fetchDays_qyy.mo?firstDay=", # 2016-12-15 needed 
    "course_table":"http://mapp.nju.edu.cn/mobile/fetchKCB_qyy.mo?firstDay=",
}

def set_cookie():
    s=requests.session()
    if not request.cookies["iPlanetDirectoryPro"]:
        return json.dumps({
            "status":"not logged in", 
        })
    s.cookies["iPlanetDirectoryPro"] = request.cookies["iPlanetDirectoryPro"]
    return s

@app.route("/api/pe_card")
def pe_card():
    s=set_cookie()
    terms_date = json.loads(s.get(urls["termDate"]).content.decode())["data"][0]
    start_date = terms_date["beginDate"]
    end_date = terms_date["endDate"]
    return s.get(urls["peCard"],params={"startDate":start_date, "endDate":end_date}).content.decode()

@app.route("/api/trans_info")
def transInfo():
    return set_cookie().get(urls["transInfo"]).content.decode()

@app.route("/api/card_info")
def cardInfo():
    return set_cookie().get(urls["cardInfo"]).content.decode()

@app.route("/api/weeks_info")
def week_info():
    return set_cookie().get(urls["weeksInfo"]).content.decode()

@app.route("/api/course_table")
def course_table():
    week = request.args.get("week")
    if not week:
        return json.dumps({
            "status":"error",
            "description":"Please set week by week=",
        })
    s=set_cookie()
    weeks = json.loads(s.get(urls["weeksInfo"]).content.decode())
    first_day = weeks["data"][int(week)-1]["firstDay"]

    courses=s.get(urls["course_table"]+first_day).content.decode()
    return json.dumps({
        "status":"success",
        "courses": courses,
    },ensure_ascii=False)

@app.route("/api/login",method=["GET","POST"])
def api_login():
    login_url="http://cer.nju.edu.cn/amserver/UI/Login"
    filename="api" + str(datetime.datetime.now().timestamp())
    captcha_path = os.path.join(os.path.dirname(__file__), "static/temp/{0}.jpg".format(filename))
    if os.path.exists(session["captcha_path"]):
        os.remove(session["captcha_path"])
    if request.method=="GET":
        s=requests.session()
        captcha = "http://cer.nju.edu.cn/amserver/verify/image.jsp"
        r = s.get(captcha,stream=True)
        with open(captcha_path,"wb+") as f:
            for chunk in r.iter_content(chunk_size=1024):
                f.write(chunk)
        session["login_cookies"]=requests.utils.dict_from_cookiejar(s.cookies)
        session["captcha_path"]=captcha_path
        return send_file(captcha_path)

    if request.method=="POST":
        captcha = request.form["captcha"]
        data={
            "encoded":"false",
            "goto":"",
            "gotoOnFail":"",
            "IDToken0":"",
            "IDButton":"Submit", 
            "IDToken1":request.form["username"], 
            "IDToken2":request.form["password"], 
            "inputCode":captcha, 
            "gx_charset":"UTF-8"
        }
        s=requests.session()
        s.cookies=requests.utils.cookiejar_from_dict(session["login_cookies"])
        s.post(login_url,data)
        session["logged_cookies"]=requests.utils.dict_from_cookiejar(s.cookies)

        return json.dumps({
            "iPlanetDirectoryPro":requests.utils.dict_from_cookiejar(s.cookies)["iPlanetDirectoryPro"]
        })

@app.route("/pecard")
def pecard():
    return render_template("pecard.html")

@app.route("/websites")
def websites():
    return render_template("websites.html")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/course_table",methods=["GET","POST"])
def course():
    if request.method=="POST":
        # username=request.form["username"]
        # password=request.form["password"]
        session=l()
        response=session.get(login.urls["course_table"])
        content=BeautifulSoup(response.content.decode("utf-8"))
        t=content.table.find("tr",align="left").table
        #return t.prettify()
        #return t.find_all("tr")[1].get_text()
        list_of_course=[]
        courses=t.find_all("tr")
        for i in range(1,len(courses)-1):
            list_of_course.append(course_table.Course.parse(courses[i].prettify()).toJSON())
        return json.dumps(list_of_course,ensure_ascii=False)
    else:
        return render_template("tables.html")
    
@app.route("/register",methods=["GET","POST"])
def register():
    if request.method=="GET":
        render_template("register.html")
    else:
        name=request.form["name"]
        student_id=request.form["student_id"]

@app.route("/school_card")
def school_card():
    return render_template("money.html")

@app.route("/login",methods=["GET","POST"])
def logins():
    login_url="http://cer.nju.edu.cn/amserver/UI/Login"
    filename=datetime.datetime.now().timestamp()
    captcha_path = os.path.join(os.path.dirname(__file__), "static/temp/{0}.jpg".format(filename))
    if os.path.exists(session["captcha_path"]):
        os.remove(session["captcha_path"])
    if request.method=="GET":
        s=requests.session()
        captcha = "http://cer.nju.edu.cn/amserver/verify/image.jsp"
        r = s.get(captcha,stream=True)
        with open(captcha_path,"wb+") as f:
            for chunk in r.iter_content(chunk_size=1024):
                f.write(chunk)
        session["login_cookies"]=requests.utils.dict_from_cookiejar(s.cookies)
        session["captcha_path"]=captcha_path
        return render_template("/login.html",img=url_for("static",filename="temp/{0}.jpg".format(filename)))

    if request.method=="POST":
        captcha = request.form["captcha"]
        data={
            "encoded":"false",
            "goto":"",
            "gotoOnFail":"",
            "IDToken0":"",
            "IDButton":"Submit", 
            "IDToken1":request.form["username"], 
            "IDToken2":request.form["password"], 
            "inputCode":captcha, 
            "gx_charset":"UTF-8"
        }
        s=requests.session()
        s.cookies=requests.utils.cookiejar_from_dict(session["login_cookies"])
        s.post(login_url,data)
        session["logged_cookies"]=requests.utils.dict_from_cookiejar(s.cookies)

        resp = make_response(redirect("/"))
        resp.set_cookie("AMAuthCookie",requests.utils.dict_from_cookiejar(s.cookies)["AMAuthCookie"])
        resp.set_cookie("iPlanetDirectoryPro",requests.utils.dict_from_cookiejar(s.cookies)["iPlanetDirectoryPro"])
        return resp
