$(document).ready(function () {
 
    function refreshPage() {
        $.ajax({
            url: "/update_flow_rack",
            type: "GET",
       
             success: function (data) {
                //  console.log('update Table >> flow rack', data); // TODO
                 updateTable(data);
            },
            error: function (error) {
                // alert("error");
                console.log("Error in refreshPage()", error);
            }
        })

    function updateTable(data) {
        var flowRacks = JSON.parse(data);
        // console.log('flowRacks', flowRacks);
        $("#flow-rack-no").text(`対象フローラックNo：${flowRacks["id"]} `);

        var flowRacktable = $('#flow-rack')
        flowRacktable.empty();
        var rack = flowRacks["rack"];

        // console.log('Rack >>', rack);

        let kanban_ids = [];
        let case_quantities = [];

        Object.keys(rack).forEach((key) => {
            if (rack[key] == "None") {
                kanban_ids.push("-");
                case_quantities.push("-");
            }
            else {
                kanban_ids.push(rack[key].part.kanban_id);
                case_quantities.push(rack[key].case_quantity);
            };
        });

        let flowRackData = `
            <tbody>
                <tr>
                    <td>
                        <div class="rack1">
                            <div id="name">ラック1</div>
                            <div id="part-id">${kanban_ids[0]}</div>
                            <div class="count">
                                <p>数量</p>
                                <p id="num">${case_quantities[0]}</p>
                            </div>
                        </div>
                    </td>
                    <td>
                        <div class="rack2">
                            <div id="name">ラック2</div>
                            <div id="part-id">${kanban_ids[1]}</div>
                            <div class="count">
                                <p>数量</p>
                                <p id="num">${case_quantities[1]}</p>
                            </div>
                        </div>
                    </td>
                </tr>
                <tr>
                    <td>
                        <div class="rack3">
                            <div id="name">ラック3</div>
                            <div id="part-id">${kanban_ids[2]}</div>
                            <div class="count">
                                <p>数量</p>
                                <p id="num">${case_quantities[2]}</p>
                            </div>
                        </div>
                    </td>
                    <td>
                        <div class="rack4">
                            <div id="name">ラック4</div>
                            <div id="part-id">${kanban_ids[3]}</div>
                            <div class="count">
                                <p>数量</p>
                                <div id="num">${case_quantities[3]}</div>
                            </div>
                        </div>
                    </td>
                </tr>
            </tbody>`;

            flowRacktable.append(flowRackData); 
    };

    }
    // 定期実行 TODO: comment out
    // setInterval(refreshPage, 500); 
    $('#refreshButton').on('click', function () {
        refreshPage();
    });
});

function complete() {
    const result = confirm(`作業を完了します`);
    if (result) {
        $.ajax({
            url: "/complete",
            type: "POST",
            contentType: "application/json",
            data: JSON.stringify({}),
            success: function (data) {
                if (data["status"] === "success") {
                    
                    setTimeout(() => {
                        $.ajax({
                            url: "/return_index",
                            type: "GET",
                            success: function (data) {
                                window.top.location.href = "/"
                            },
                            error: function (error) {
                                // alert("error");
                                console.log("Error in Flow rack js", error)

                            }
                        });

                    }, 500);
                } else {
                    alert("no flow racks");
                }
            },
            error: function (error) {
                // alert(error.status + ": " + error.responseText)
                console.log("Error >>", error.status + ": " + error.responseText)
            }
        });
    }
}
