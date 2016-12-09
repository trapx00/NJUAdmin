function updatePEInfo(){
    $.get("/api/pe_card",function(data){
        let counter = 1;
        let parsedData=JSON.parse(data)["data"];
        $("#times").text(parsedData["msg"]+"/30");
        let newData = [];
        parsedData["data"].forEach(function(record){
            console.log(record);
            let time = record["transtime"];
            let date = record["transdate"];
            let device = record["devicename"];
            let period = record["period"];
            let formatedRecord = {};
            formatedRecord.id =counter;
            counter++;
            formatedRecord.time = formatString(date,time);
            formatedRecord.device = device;
            newData.push(formatedRecord);
        });
        console.log(newData);
        $("#details").bootstrapTable({
            data: newData,
            columns:[{
                field:"id",
                title:"#",
            },{
                field: "time",
                title : "时间", 
            },{
                field: "device",
                title:"设备名称",
            }]
        });
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