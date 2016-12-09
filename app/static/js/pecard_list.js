function updatePEInfo(){
    $.get("/api/pe_card",function(data){
        let counter = 1;
        let parsedData=JSON.parse(data)["data"];
        $("#times").text(parsedData["msg"]+"/30");
        console.log(parsedData["data"]);
        $("table").bootstrapTable({
            data: parsedData["data"],
            columns:[{
                field: "transtime",
                title : "时间", 
            },{
                field: "devicename",
                title:"设备名称",
            }]
        });

        // parsedData["data"].reverse().forEach(function(record){
        //     let time = record["transtime"];
        //     let date = record["transdate"];
        //     let device = record["devicename"];
        //     let period = record["period"];
        //     let element = $("<tr></tr>");
        //     element.append($("<td></td>",{
        //         text:counter
        //     }));
        //     counter++;
        //      element.append($("<td></td>",{
        //         text:formatString(date,time)
        //     }));
        //     element.append($("<td></td>",{
        //         text:device
        //     }));
        //     $("#pecard_list").append(element);
        // });
    });
 
}

function formatString(date,time){
    let year = date.substring(0,4);
    let month = date.substring(4,6);
    let day = date.substring(6,8);
    let hour = time.substring(0,2);
    let minute = time.substring(2,4);
    let second = time.substring(4,6);
    let datetime = "{0}年{1}月{2}日 {3}:{4}:{5}".format(year,month,day,hour,minute,second);
    return datetime;
}

updatePEInfo();