from enum import Enum
from bs4 import BeautifulSoup
import json,re,jsonpickle
import simplejson as json
#周五 第3-4节 4-17周 仙Ⅱ-304
#周五 第7-8节 从第5周开始:单周 仙Ⅱ-207
					  
translation={
    "周一":1,
    "周二":2,
    "周三":3,
    "周四":4,
    "周五":5, 
    "周六":6, 
    "周日":7,
}


class CourseTimeAndLocation():
    def __init__(self,weekday=None,start_time=None,end_time=None,weeks=None,location=None):
        self.weekday=weekday
        self.start_time=start_time
        self.end_time=end_time
        self.weeks=weeks
        self.location=location
    
    def parse(description:str):
        '''Parses a formatted string to a CourseTimeAndLocation object
        Allowed formats: (used in 2016-12-4)
        周五 第3-4节 4-17周 仙Ⅱ-304
        周五 第7-8节 从第5周开始:单周 仙Ⅱ-207 

        Args:
        description: formatted string
        return_json: If set to false, it returns a CourseTimeAndLocation object, otherwise, it returns json.dumps(CourseTimeAndLocation object).

        Returns:
        None if the string contains 自由
        A CourseTimeAndLocation Object or json string 
        '''
        if "自由" in description:
            return None
        content=description.split()
        weekday=translation[content[0]]
        start_time=int(content[1].split("-")[0].replace("第",""))
        end_time=int(content[1].split("-")[1].replace("节",""))

        if "单" in content[2] or "双" in content[2]:
            start_week=int(content[2][2])
            weeks=list(range(start_week,17,2))
        else:
            start_week=int(content[2].split('-')[0])
            end_week=int(content[2].split('-')[1].replace("周",""))
            weeks=list(range(start_week,end_week))
        
        if len(content)>3:
            location=content[3]
        else:
            location=""
        
        return CourseTimeAndLocation(weekday,start_time,end_time,weeks,location)
    
    def toJSON(self):
        jsonpickle.set_preferred_backend("simplejson")
        jsonpickle.set_encoder_options('simplejson', ensure_ascii=False)
        return jsonpickle.encode(self)

class Course():
    def __init__(self,name=None,teachers=None,number=None,course_time_location=None,exam_time=None,school_district=None):
        self.name=name
        self.teachers=teachers
        self.number=number
        self.course_time_location=course_time_location
        self.exam_time=exam_time
        self.school_district=school_district
    
    def parse(html_content:str):
        '''Parses formatted raw html_content to a Course object
        
        Args:
        html_content: html strings, not BeautifulSoup object
    
        Returns:
        A Course object
        '''
        soup=BeautifulSoup(html_content.replace("\n",""))
        all_nodes=soup.find_all("td")

        number=all_nodes[0].text.strip()
        name=all_nodes[2].text.strip()
        school_district=all_nodes[3].text.strip()
        teachers=all_nodes[4].text.strip()
        course_time_location=[]
        time=all_nodes[5]

        if time.find("br"):
            times=str(time).split('<br/>')
            pattern="<[\s\S]*>"
            for i in times:
                l=re.sub(pattern,"",i).strip()
                course_time_location.append(CourseTimeAndLocation.parse(l))
        else:
            course_time_location.append(CourseTimeAndLocation.parse(time.text.strip()))

        exam_time=all_nodes[9].get_text()
        #return time
        #return (name,teachers,number,course_time_location,exam_time,school_district)
        return Course(name,teachers,number,course_time_location,exam_time,school_district)

    def toJSON(self):
        jsonpickle.set_preferred_backend("simplejson")
        jsonpickle.set_encoder_options('simplejson', ensure_ascii=False)
        return jsonpickle.encode(self)


        