/// <reference path="jquery.d.ts" />

interface CourseTimeLocation{

}

interface Course{
    name,teachers,number,exam_time,school_district : string;
    course_time_location:CourseTimeLocation;

}


function clearTable() {
    $("#course_table tr").slice(1).each(function () {
        $("td", this).slice(1).each(function () {
            $(this).text("");
        })
    })
}


function writeTable(data: Array<string>) {
    clearTable();
    var week: number = parseInt($("#week").val());
    data.forEach(function (json_course: string) {
        var course = JSON.parse(json_course);
        course["course_time_location"].forEach(function (time_location) {
            if (!time_location || !time_location["weeks"].includes(week)) 
                return;
            for (let i = parseInt(time_location["start_time"]); i <= parseInt(time_location["end_time"]); i++) {
                let selector = `#course_table tr:eq(${i}) td:eq(${time_location["weekday"]})`;
                $(selector).append(constructCourse(course, time_location));
            }
        }
        )
    });
}

function requireCourseTable() {
    var username: string = $("#username").val();
    var password: string = $("#password").val();

    var url:string = "/course_table";
    var data = { "username": username, "password": password };

    $.post(url, data, writeTable, "json"); //data is a form
}

function constructCourse(course: Course, time_location: CourseTimeLocation) {
    var element = $("<a></a>", {
        text: course["name"],
        rel: "popover",
    });
    var pop_content = `${course["name"]}<br/>老师：${course["teachers"]}<br/>地点：${course["location"]}`;
    element.attr("data-content", pop_content);
    element.attr("tabindex", "0");
    element.attr("data-trigger", "focus");
    element.attr("data-html", "true");
    element.attr("onclick", "$(this).popover();");
    element.attr("class", "btn btn-default btn-block");
    return element;
}
