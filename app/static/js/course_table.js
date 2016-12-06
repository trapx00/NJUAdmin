////// <reference path="../relative/path/to/jquery.d.ts"/>

var colors = {
    "仙Ⅱ": "#B0C4DE",
    "仙Ⅰ": "#87CEEB",
    "逸A": "#48D1CC",
    "逸B": "#D2B48C",
}

String.prototype.format = function () {
    var args = arguments;
    return this.replace(/\{(\d+)\}/g, function (s, i) {
        return args[i];
    });
}

function clearTable() {
    $("#course_table tr").slice(1).each(function () {
        $("td", this).slice(1).each(function () {
            $(this).text("");
            $(this).removeAttr("bgcolor");
        })
    })
}

function changeWeek(offset) {
    let current_week = parseInt($("#week").val());
    if ((current_week <= 0 && offset < 0) || (current_week >= 20 && offset > 0))
        alert("周数不对了吧");
    else {
        $("#week").val(current_week + offset);
    }
    writeTable();
}

function writeTable() {
    toggleNoon();
    clearTable();
    var week = parseInt($("#week").val());
    var data = window.localStorage["course_table"];
    if (!data) {
        requireCourseTable();
    }
    JSON.parse(data).forEach(function (json_course) {
        var course = JSON.parse(json_course);
        course["course_time_location"].forEach(function (time_location) {
            if (!time_location || !time_location["weeks"].includes(week)) return;
            for (let i = parseInt(time_location["start_time"]); i <= parseInt(time_location["end_time"]); i++) {
                let selector = "#course_table tr:eq({0}) td:eq({1})".format(i, time_location["weekday"]);
                $(selector).text(course["name"]);
                let building = time_location["location"].split("-")[0];
                let color = "#FFFFFF";
                if (building in colors) color = colors[building];
                $(selector).attr("bgcolor",color);
                $(selector).attr("onclick",'displayModal("{0}","{1}","{2}");'.format(course["name"], course["teachers"], time_location["location"]));
                //$(selector).append(constructCourse(course, time_location));
            }
        }
        )
    });
    toggleNoon();
}

function setCurrentWeek() {
    let current_day = new Date();
    let start_day = Date.parse("Aug 28, 2016");

    let weeks = Math.ceil((current_day - start_day) / (24 * 3600 * 1000 * 7))
    $("#week").val(weeks);
}

function refresh() {
    window.localStorage['course_table'] = '';
    clearTable();
    requireCourseTable();
}

function requireCourseTable() {
    var username = $("#username").val();
    var password = $("#password").val();

    var url = "/course_table";
    var data = { "username": username, "password": password };

    $.post(url, data, (data) => {
        window.localStorage["course_table"] = data;
        writeTable();
    }); //data is a form
}

function displayModal(name, teachers, location) {
    var dialog = $("#detailed");
    $("#name", dialog).text(name);
    $("#teachers", dialog).text("老师：" + teachers);
    $("#location", dialog).text("上课地点：" + location);
    dialog.modal();
}

function toggleNoon() {
    if ($("#noon").length === 0) {
        var tr = $("<tr></tr>", {
            class: "gradeA even",
            role: "row",
            id: "noon",
        });
        var td = $("<td></td>", {
            colspan: "8",
        });
        var p = $("<p></p>", {
            class: "text-center",
            text: "午休(12:00~2:00) 睡觉去！"
        });
        td.append(p);
        tr.append(td);
        $("#course_table tr:eq(4)").after(tr);
    }
    else {
        $("#noon").remove();
    }
}