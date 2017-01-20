import requests

urls = {
    "login_jw": "http://jw.nju.edu.cn:8080/jiaowu/login.do",
    "login_platform" : "http://cer.nju.edu.cn/amserver/UI/Login", 
    "course_table": "http://jw.nju.edu.cn:8080/jiaowu/student/teachinginfo/courseList.do?method=currentTermCourse",
    "course_table_platform":"http://mapp.nju.edu.cn/mobile/fetchKCB_qyy.mo?firstDay=2016-12-05", 
    "index": "http://jw.nju.edu.cn:8080/jiaowu/student/index.do",
    "grades": "http://jw.nju.edu.cn:8080/jiaowu/student/studentinfo/achievementinfo.do?method=searchTermList", #termCode= year+(1|2)
}


def login_eduadmin(username: str, password: str)->requests.session:
    data = {
        "userName": username,
        "password": password,
        "returnUrl": "null"
    }
    session = requests.session()
    session.post(urls["login_jw"], data)
    return session


def login_platform(username, password):
    session=requests.session()
    return session.get(urls["login_platform"])
