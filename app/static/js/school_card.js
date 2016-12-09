function updateTransInfo(){
    $.get("/api/card_info",function(data){
        $("#balance").text(JSON.parse(data)["data"]["balance"]);
    });
    $.get("/api/trans_info",{"size":"30"},function(data){
        let counter = 1;
        let parsedData=JSON.parse(data)["data"];
        console.log(parsedData);
        $("#detailed").bootstrapTable({
            data: parsedData["items"],
            columns:[{
                field:"transTime",
                title:"发生时间",
            },{
                field: "termName",
                title : "地点", 
            },{
                field: "amount",
                title:"金额",
            },{
                field:"balance",
                title:"余额",
            }]
        });
    });
}

function changeTheNumberOfItems(){
    $.get("/api/trans_info",{"size":"30"},function(data){
        let counter = 1;
        let parsedData=JSON.parse(data)["data"];
        console.log(parsedData);
        $("#detailed").bootstrapTable({
            data: parsedData["items"],
            columns:[{
                field:"transTime",
                title:"发生时间",
            },{
                field: "termName",
                title : "地点", 
            },{
                field: "amount",
                title:"金额",
            },{
                field:"balance",
                title:"余额",
            }]
        });
    });

}
updateTransInfo();