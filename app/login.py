import requests

urls = {
    "login": "http://jw.nju.edu.cn:8080/jiaowu/login.do",
    "login_platform" : "http://cer.nju.edu.cn/amserver/UI/Login", 
    "course_table": "http://jw.nju.edu.cn:8080/jiaowu/student/teachinginfo/courseList.do?method=currentTermCourse",
    "course_table_platform":"http://mapp.nju.edu.cn/mobile/fetchKCB_qyy.mo?firstDay=2016-12-05", 
    "index": "http://jw.nju.edu.cn:8080/jiaowu/student/index.do",
}


def login_eduadmin(username: str, password: str)->requests.session:
    data = {
        "userName": username,
        "password": password,
        "returnUrl": "null"
    }
    session = requests.session()
    session.post(urls["login"], data)
    return session

'''encoded=true&goto=aHR0cDovL3ZvbHVudGVlci5uanUuZWR1LmNuOjgwLw%3D%3D&gotoOnFail=&IDToken0=&IDButton=Submit&IDToken1=161250010&IDToken2=Cqwzcjd123-&inputCode=BPFD&gx_charset=UTF-8'

encoded=false&goto=&gotoOnFail=&IDToken0=&IDButton=Submit&IDToken1=161250010&IDToken2=Cqwzcjd123-&inputCode=bdfa&gx_charset=UTF-8

encoded=false&goto=&gotoOnFail=&IDToken0=&loginLT=885378e8-5b39-4a60-b129-3e430ebc7740&IDButton=Submit&username=161250010&password=Cqwzcjd123-&gx_charset=UTF-8


encoded=false&goto=&gotoOnFail=&IDToken0=&loginLT=1fd0b66a-4129-49e0-ae85-d092abf3c1d2&IDButton=Submit&username=161250010&password=Cqwzcjd123-&gx_charset=UTF-8
username=161250010&encoded=false&goto=&IDToken0=&gotoOnFail=&gx_charset=UTF-8&password=Cqwzcjd123-&IDButton=Submit

http://cer.nju.edu.cn/amserver/UI/Login?goto=http%3A%2F%2Fimp.nju.edu.cn%2Fimp%2FauthLogin.do&gotoOnFail=http%3A%2F%2Fimp.nju.edu.cn%2Fimp%2FfailLogin.do
'''

def login_platform(username="161250010", password="Cqwzcjd123-"):
    session=requests.session()
    return session.get(urls["login_platform"])
