function updateTransInfo(){
    $.get("/api/card_info",function(data){
        $("#balance").text(JSON.parse(data)["data"]["balance"]);
    });
    $.get("/api/trans_info",function(data){
        let counter = 1;
        let parsedData=JSON.parse(data)["data"];
        console.log(parsedData);
        parsedData["items"].forEach(function(record){
            let time = record["transTime"];
            let place = record["termName"];
            let amount = record["amount"];
            let balance = record["balance"];
            let element = $("<tr></tr>");
            element.append($("<td></td>",{
                text:counter
            }));
            counter++;
             element.append($("<td></td>",{
                text:time
            }));
            element.append($("<td></td>",{
                text:place
            }));
            element.append($("<td></td>",{
                text:amount
            }));
            element.append($("<td></td>",{
                text:balance
            }));
            $("#pecard_list").append(element);
        });
    });
}

updateTransInfo();