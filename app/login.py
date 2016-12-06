import requests

urls = {
    "login": "http://jw.nju.edu.cn:8080/jiaowu/login.do",
    "course_table": "http://jw.nju.edu.cn:8080/jiaowu/student/teachinginfo/courseList.do?method=currentTermCourse",
    "index": "http://jw.nju.edu.cn:8080/jiaowu/student/index.do",
}


def login(username: str, password: str)->requests.session:
    """Login 
Log in NJU education administration system with username and password provided.

Args:
username: string,
password: string,

Returns:
A requests.session Object
"""
    data = {
        "userName": username,
        "password": password,
        "returnUrl": "null"
    }
    session = requests.session()
    session.post(urls["login"], data)
    return session
