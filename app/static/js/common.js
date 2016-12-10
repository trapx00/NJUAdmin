function logOut() {
    Cookies.remove("iPlanetDirectoryPro");
    window.location.href = "/";
}

function init() {
    checkLogIn();
    updateHeaderInfo()
}

function checkLogIn() {
    if (!Cookies.get("iPlanetDirectoryPro")) {
        $(".logged_in").hide();
        $("#not_logged").show();
    } else {
        $(".logged_in").show();
        $("#not_logged").hide();
    }
}

function updateHeaderInfo() {
    if (Cookies.get("iPlanetDirectoryPro")) {
        let weeksInfo = window.localStorage["weeksInfo"];
        if (weeksInfo) {
            let currentWeek = weeksInfo.split("/")[0],
                totalWeek = weeksInfo.split("/")[1];
            $("#date").text("这是第" + currentWeek + "/" + totalWeek + "周");
        }
        else {
            $.get("/api/weeks_info", function (data) {
                var parsedData = JSON.parse(data);
                var prompt = "这是第" + parsedData["currentWeek"] + "/" + parsedData["totalWeek"] + "周";
                $("#date").text(prompt);
                window.localStorage["weeksInfo"]=parsedData["currentWeek"] + "/" + parsedData["totalWeek"];
            });

        }
    }
}

String.prototype.format = function () {
    var args = arguments;
    return this.replace(/\{(\d+)\}/g, function (s, i) {
        return args[i];
    });
}
