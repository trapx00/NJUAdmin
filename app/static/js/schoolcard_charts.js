function updateCharts() {
    $.get("/api/trans_info", { "size": $("#data_amount").val() }, function (data) {
        let parsedData = JSON.parse(data)["data"];
        let chartsData = [];
        parsedData["items"].forEach(function (record) {
            let timestamp = parseToTimeStamp(record["transTime"]);
            let oneRecord = [parseInt(timestamp), parseFloat(record["balance"])];
            chartsData.push(oneRecord);
        });
        console.log(parsedData);
        console.log(chartsData);
        window.localStorage["parsedData"] = JSON.stringify(parsedData);
        // for (var i = 0; i < 30; i += 0.5){ chartsData.push([i, Math.sin(i)]); } 
        if (window.plot) {
            window.plot.setData([chartsData]);
            window.plot.setupGrid();
            window.plot.draw();
            return;
        }
        $(document).ready(function () {
            window.plot = $.plot($("#placeholder"), [chartsData], {
                xaxis: {
                    mode: "time",
                    timeformat: "%m/%d",
                    timezone: "browser",
                },
                series: {
                    points: {
                        show: true,
                        fill: true,
                    },
                    lines: {
                        show: true,
                        fill: false,
                    }
                },
                grid: {
                    hoverable: true,
                    clickable: true,
                },
            });
        })

    });
}
$("#placeholder").bind("plothover", function (event, position, item) {
    if (item) {
        var x = item.datapoint[0].toFixed(2),
            y = item.datapoint[1].toFixed(2);

        let parsedData = JSON.parse(window.localStorage["parsedData"]);

        $("#tooltip").html(constructPopUp(parsedData["items"][item.dataIndex]))
            .css({ top: item.pageY + 5, left: item.pageX + 5 })
            .fadeIn(200);
    } else {
        $("#tooltip").hide();
    }
});
$("#placeholder").bind("plotclick", function (event, position, item) {
    if (item) {
        var x = item.datapoint[0].toFixed(2),
            y = item.datapoint[1].toFixed(2);

        let parsedData = JSON.parse(window.localStorage["parsedData"]);

        $("#tooltip").html(constructPopUp(parsedData["items"][item.dataIndex]))
            .css({ top: item.pageY + 5, left: item.pageX + 5 })
            .fadeIn(200);
    } else {
        $("#tooltip").hide();
    }
});
$("#placeholder").resize(function () {
    $(".message").text("Placeholder is now "
        + $(this).width() + "x" + $(this).height()
        + " pixels");
});


function constructPopUp(item) {
    let popup = "时间：" + item["transTime"] + "<br>地点：" + item["termName"] + "<br>变化：" + item["amount"] + "<br>余额：" + item["balance"];
    return popup;
}

function parseToTimeStamp(time) {
    //16-11-24 17:09
    let pattern = "YYYY-MM-DD HH:MM";
    let date = Date.parse("20" + time, pattern);
    return date;
}

$("<div id='tooltip'></div>").css({
    position: "absolute",
    display: "none",
    border: "1px solid #fdd",
    padding: "2px",
    "background-color": "#fee",
    opacity: 0.80
}).appendTo("body");

$("#data_amount").change(function () {
    updateCharts();
});
updateCharts();
