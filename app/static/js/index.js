////// <reference path="jquery.d.ts"/>

function updateInfo(){
    $.get("/api/pe_card",function(data){
        var data = JSON.parse(data)["data"]["msg"];
        $("#pe_time").text(data.includes("未查询到") ? "Failed" : data+"/30");
        
    });
    $.get("/api/card_info",function(data){
        $("#balance").text(JSON.parse(data)["data"]["balance"]);
        $("#greetings").text("你好！" + JSON.parse(data)["data"]["name"]);
    });

}

updateInfo();