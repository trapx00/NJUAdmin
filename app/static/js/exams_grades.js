

function updateGradesInfo() {
    var formData = new FormData();
    var invert = false;
    var termCode = $("#termsList").val();
    if (termCode === "0") {
        return;
    }
    formData.append("username", atob(Cookies.get("username")));
    formData.append("password", atob(Cookies.get("password")));
    formData.append("termCode", termCode);
    table.destroy();
    $.ajax({
        url: "/api/exam_grades",
        data: formData,
        type: "POST",
        processData: false,
        contentType: false,
        success: function (data) {
            var parsedData = JSON.parse(data);
            var totalScore1 = 0, totalMark1 = 0; //without 选修
            var totalScore2 = 0, totalMark2 = 0; //with 选修
            table = $("#grades").DataTable({
                data: parsedData,
                columns: [
                    { data: 'chn_name' },
                    { data: 'type' },
                    { data: 'score' },
                    { data: "mark" },
                ],
                lengthChange: false,
                paging: false,
                info: false,
                searching: false,
            });
            parsedData.forEach(function (course) {
                if (course.type != "选修" || course.chn_name.includes("英语")) {
                    totalScore1 += parseInt(course.score);
                    totalMark1 += parseInt(course.mark) * parseInt(course.score);
                }
                totalScore2 += parseInt(course.score);
                totalMark2 += parseInt(course.mark) * parseInt(course.score);
            });
            $("#gpa1").text((totalMark1/totalScore1/20).toFixed(3));
            $("#gpa2").text((totalMark2/totalScore2/20).toFixed(3));
        }
    });
}

function updateTermsList() {
    var formData = new FormData();
    var invert = false;
    formData.append("username", atob(Cookies.get("username")));
    formData.append("password", atob(Cookies.get("password")));
    $.ajax({
        url: "/api/valid_terms",
        data: formData,
        type: "POST",
        processData: false,
        contentType: false,
        success: function (data) {
            console.log(data);
            var parsedData = JSON.parse(data);
            var greatestValue =0;
            parsedData.forEach(function (term) {
                var year = term.substring(0, 4);
                var termNo = term[4];
                var disp = "{0}-{1}年第{2}学期".format(year, parseInt(year) + 1, termNo);
                $("#termsList").append("<option value='{0}'>{1}</option>".format(term, disp));
                if (greatestValue < parseInt(term)){
                    greatestValue = parseInt(term);
                }
            });
            $("option[value='{0}']".format(greatestValue)).attr("selected","selected");
            updateGradesInfo();
        }
    });
}

function loginEduAdmin() {
    $.post("/api/login_eduadmin", $("#login_form").serialize(), function (msg) {
        var parsedData = JSON.parse(msg);
        if (parsedData["status"] === "error") {
            $(".col-lg-12:eq(1) .row:eq(1)").show();
        }
        if (parsedData["status"] === "success") {
            Cookies.set("username", btoa($("#username").val()));
            Cookies.set("password", btoa($("#password").val()));
            window.location.reload();
        }
    });
}

function checkEduAdminLogin() {
    if (Cookies.get("username") && Cookies.get("password")) {
        $(".col-lg-12:first").show();
        updateTermsList();
    }
    else {
        $(".col-lg-12:eq(1) .row:lt(2)").hide();
        $(".col-lg-12:first").hide();
    }
}

function eduadminLogout(){
    Cookies.remove("username");
    Cookies.remove("password");
    window.location.reload();
}

checkEduAdminLogin();

$("#termsList").change(function () {
    updateGradesInfo();
});

var table = $("#grades").DataTable({
    lengthChange: false,
    paging: false,
    info: false,
    searching: false
});