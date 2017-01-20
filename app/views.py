from app import app,login,course_table
from bs4 import BeautifulSoup
import json, requests, os, http.cookiejar, datetime
from flask import render_template,request, url_for, g, session, redirect, make_response, send_file, jsonify

urls = {
    "peCard": "http://mapp.nju.edu.cn/mobile/getExerciseInfo.mo", #start and end time needed startDate=2016-08-29&endDate=2017-01-08
    "termDate": "http://mapp.nju.edu.cn/mobile/getTermDateInfo.mo", #included all term date
    "cardInfo": "http://mapp.nju.edu.cn/mobile/getCardInfo.mo",
    "transInfo":"http://mapp.nju.edu.cn/mobile/getTransList.mo", #pageSize can be provided and page
    "weeksInfo":"http://mapp.nju.edu.cn/mobile/fetchWeek_qyy.mo", 
    "days":"http://mapp.nju.edu.cn/mobile/fetchDays_qyy.mo?firstDay=", # 2016-12-15 needed 
    "course_table":"http://mapp.nju.edu.cn/mobile/fetchKCB_qyy.mo?firstDay=",
}

def set_cookie():
    s=requests.session()
    if not "iPlanetDirectoryPro" in request.cookies:
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
    size = request.args.get("size")
    return set_cookie().get(urls["transInfo"],params={"pageSize":size}).content.decode()

@app.route("/api/card_info")
def cardInfo():
    return set_cookie().get(urls["cardInfo"]).content.decode()

@app.route("/api/weeks_info")
def week_info():
    return set_cookie().get(urls["weeksInfo"]).content.decode()

@app.route("/api/course_table")
def api_course_table():
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

@app.route("/api/login",methods=["GET","POST"])
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

@app.route("/api/exam_schedules",methods=["POST"])
def api_exam_schedules():
    username = request.form.get("username")
    password=request.form.get("password")
    if not username or not password:
        return json.dumps({
            "status":"error",
            "description":"not logged in"
        })
    return json.dumps(course_table.get_exams_schedules(username,password),ensure_ascii=False)

@app.route("/api/exam_grades",methods=["POST"])
def api_exam_grades():
    username = request.form.get("username")
    password=request.form.get("password")
    code=request.form.get("termCode")
    return json.dumps(course_table.get_grades(username,password,code),ensure_ascii=False)

@app.route("/api/valid_terms",methods=["POST"])
def api_valid_terms():
    username = request.form.get("username")
    password=request.form.get("password")
    if not username or not password:
        return json.dumps({
            "status":"error",
            "description":"not logged in"
        })
    return json.dumps(course_table.get_valid_terms(username,password),ensure_ascii=False)

@app.route("/pecard")
def pecard():
    return render_template("pecard.html")

@app.route("/websites")
def websites():
    return render_template("websites.html")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/communication")
def communication():
    return render_template("communication.html")
    
@app.route("/register",methods=["GET","POST"])
def register():
    if request.method=="GET":
        render_template("register.html")
    else:
        name=request.form["name"]
        student_id=request.form["student_id"]

@app.route("/plugins",methods=["GET","POST"])
def plugins():
    return render_template("plugins.html")

@app.route("/schoolcard/data")
def school_card():
    return render_template("schoolcard.html")

@app.route("/schoolcard/charts")
def schoolcard_charts():
    return render_template("schoolcard_charts.html")

@app.route("/exams/schedules",methods=["GET"])
def exams_schedules():
    return render_template("exams_schedules.html")
    
@app.route("/api/login_eduadmin",methods=["POST"])
def login_eduadmin():
    username = request.form["username"]
    password = request.form["password"]
    s= login.login_eduadmin(username,password)
    cookie = requests.utils.dict_from_cookiejar(s.cookies).get("user_id")
    if cookie:
        return json.dumps({
            "status":"success",
        })
    else:
        return json.dumps({
            "status":"error",
        })
@app.route("/course_table")
def new_course_table():
    return render_template("tables.html")

@app.route("/exams/grades")
def exams_grades():
    return render_template("exams_grades.html")


@app.route("/login",methods=["GET","POST"])
def logins():
    login_url="http://cer.nju.edu.cn/amserver/UI/Login"
    filename=datetime.datetime.now().timestamp()
    captcha_path = os.path.join(os.path.dirname(__file__), os.path.join("static","temp","{0}.jpg".format(filename)))
    if session.get("captcha_path") and os.path.exists(session.get("captcha_path")):
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
        if not "iPlanetDirectoryPro" in requests.utils.dict_from_cookiejar(s.cookies):
            return redirect("/login")
        resp.set_cookie("iPlanetDirectoryPro",requests.utils.dict_from_cookiejar(s.cookies)["iPlanetDirectoryPro"])
        return resp

@app.route("/about")
def about():
    return render_template("about.html")