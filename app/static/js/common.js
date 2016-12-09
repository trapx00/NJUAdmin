function logOut(){
    Cookies.remove("iPlanetDirectoryPro");  
    window.location.href="/";
}

function init(){
    checkLogIn();
    updateHeaderInfo()
}

function checkLogIn(){
    if (!Cookies.get("iPlanetDirectoryPro")){
        $(".logged_in").hide();
        $("#not_logged").show();
    } else {
        $(".logged_in").show();
        $("#not_logged").hide();
    }
}

function updateHeaderInfo(){
    if (Cookies.get("iPlanetDirectoryPro")){
        $.get("/api/weeks_info",function(data){
        var parsedData = JSON.parse(data);
        console.log(parsedData);
        $("#date").text("这是第"+parsedData["currentWeek"]+"/"+parsedData["totalWeek"]+"周");
    });
    }
}

String.prototype.format = function () {
    var args = arguments;
    return this.replace(/\{(\d+)\}/g, function (s, i) {
        return args[i];
    });
}
