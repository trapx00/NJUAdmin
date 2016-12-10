function loginEduAdmin() {
    $.post("/api/login_eduadmin", $("#login_form").serialize(), function (msg) {
        let parsedData = JSON.parse(msg);
        if (parsedData["status"] === "error") {
            $(".col-lg-6:eq(1) .row:eq(1)").show();
        }
        if (parsedData["status"] === "success") {
            Cookies.set("username", $("#username").val());
            Cookies.set("password", $("#password").val());
            window.location.reload();
        }
    });
}

function getSchedules() {
    let formData = new FormData();
    let invert = false;
    formData.append("username", Cookies.get("username"));
    formData.append("password", Cookies.get("password"));
    $.ajax({
        url: "/api/exam_schedules",
        data: formData,
        type: "POST",
        processData: false,
        contentType: false,
        success: function (msg) {
            let parsedData = JSON.parse(msg);
            parsedData = parsedData.filter(function (el) {
                return !el.exam_time.includes("请咨询");
            });

            parsedData = parsedData.sort(function (a, b) {
                let A = a.exam_time.trim();
                let B = b.exam_time.trim();

                //step 1
                let dayA = parseToTimestamp(A.split(' ')[0]);
                let dayB = parseToTimestamp(B.split(' ')[0]);
                if (dayA != dayB) {
                    return dayA - dayB;
                }

                //step 2
                let timeA = A.split(' ')[1];
                let timeB = B.split(' ')[1];


                if (timeA && timeB) {
                    let paddle
                    if (timeA.length < 5)
                        timeA = "0" + timeA;
                    if (timeB.length < 5)
                        timeB = "0" + timeB;
                    return timeA - timeB;
                }
                return 0;
            });
            $("#timeline-template").show();
            parsedData.forEach(function (item) {
                let element = $("#timeline-template").clone();
                element.removeAttr("id");
                $(".text-muted", element).html('<i class="fa fa-clock-o"></i>' + item.exam_time);
                $(".timeline-title", element).text(item.course);
                if (invert){
                    $(element).addClass("timeline-inverted");
                }
                invert=!invert;
                $(".timeline").append(element);
            });
            $("#timeline-template").hide();
        }
    });
}

function parseToTimestamp(time) {
    //16-11-24 17:09
    let pattern = "YYYY-MM-DD";
    let date = Date.parse(time, pattern);
    return date;
}


function checkEduAdminLogin() {
    if (Cookies.get("username") && Cookies.get("password")) {
        $(".col-lg-6:first").show();
        getSchedules();
    }
    else {
        $(".col-lg-6:eq(1) .row:lt(2)").hide();
        $(".col-lg-6:first").hide();
    }
}

function eduadminLogout(){
    Cookies.remove("username");
    Cookies.remove("password");
    window.location.reload();
}

checkEduAdminLogin();