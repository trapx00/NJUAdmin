function updatePEInfo() {
    $.get("/api/pe_card", function (data) {
        var counter = 1;
        var parsedData = JSON.parse(data)["data"];
        $("#pe_time").text(parsedData["msg"] + "/30");
        var newData = [];
        parsedData["data"].forEach(function (record) {
            var time = record["transtime"];
            var date = record["transdate"];
            var device = record["devicename"];
            var period = record["period"];
            var formatedRecord = {};
            formatedRecord.id = counter;
            counter++;
            formatedRecord.time = formatString(date, time);
            formatedRecord.device = device;
            newData.push(formatedRecord);
        });
        $("#detailed").DataTable({
            data: newData,
            columns: [
                { data: 'id' },
                { data: 'time' },
                { data: "device" },
            ],
        });
    });

}

function formatString(date, time) {
    var year = date.substring(0, 4);
    var month = date.substring(4, 6);
    var day = date.substring(6, 8);
    var hour = time.substring(0, 2);
    var minute = time.substring(2, 4);
    var second = time.substring(4, 6);
    var datetime = "{0}年{1}月{2}日 {3}:{4}:{5}".format(year, month, day, hour, minute, second);
    return datetime;
}

updatePEInfo();