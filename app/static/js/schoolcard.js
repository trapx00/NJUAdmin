function updateTransInfo(){
    $.get("/api/card_info",function(data){
        $("#balance").text(JSON.parse(data)["data"]["balance"]);
    });
    $.get("/api/trans_info",$("#data_amount").val(),function(data){
        let counter = 1;
        let parsedData=JSON.parse(data)["data"];
        console.log(parsedData["items"]);
        $("#detailed").DataTable({
            data:parsedData["items"],
            columns:[
                {data:'transTime'},
                {data: 'termName'},
                {data: "amount"},
                {data: "balance"},
            ],
            order: [[0,"desc"]],
        });
    });
}

function changeTheNumberOfItems(amount){
    $.get("/api/trans_info",{"size": amount},function(data){
        let parsedData=JSON.parse(data)["data"];
        $('#detailed').dataTable().fnClearTable();
        $('#detailed').dataTable().fnAddData(parsedData["items"]);
    });

}
updateTransInfo();

$("#data_amount").change(function(){
    if ($("#data_amount").val()==="-1"){
        $("#customize").show();
        return;
    }
    $("#customize").hide();
    changeTheNumberOfItems($("#data_amount").val());
});
$("#submit").click(function(){
    changeTheNumberOfItems($("#amount").val());
});