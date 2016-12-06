from app import app,login,course_table
from bs4 import BeautifulSoup
import json
from flask import render_template,request

l=lambda : login.login("161250010","162642")


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
        
