$(document).ready(function () {
 
    function refreshPage() {
        $.ajax({
            url: "/update_product_info",
            type: "GET",
          
             success: function (data) {
                // console.log('update_product_info >>', data); // TODO:
                 updateTable(data);
            },
            error: function (error) {
                console.error("Error fetching data:", error);
            }
        });

        function updateTable(data) {
            
            // var lData = JSON.parse(data[0]); // TODO: comment out
            // var rData = JSON.parse(data[1]); // TODO: comment out
            var rData = JSON.parse(data[0]); // TODO: add
            var lData = JSON.parse(data[1]); // TODO: add
            var lineData = JSON.parse(data[2]);
            let tbody1 = $('#count');
           
            tbody1.empty();

            let row1 = `
                <tr>
                    <td>${rData.product.kanban_id}</td>
                    <td>${rData.planned_num}</td>
                    <td>${rData.output_num}</td>
                    <td>${lData.product.kanban_id}</td>
                    <td>${lData.planned_num}</td>
                    <td>${lData.output_num}</td>
                </tr>`;
            tbody1.append(row1);
          
            Object.keys(lineData).forEach((key) => {

                let line = lineData[key]
                // TODO: current frontages is {}, need to ask for testing
                Object.keys(line.frontages).forEach((key) => {
                   
                    let frontage = line.frontages[key];
                    let tbody = $(`#${frontage.id}`);
                    tbody.empty();

                    Object.keys(frontage.inventories).forEach((key) => {
                        let rack = frontage.inventories[key];
                                          
                        let row = `
                        <tr>
                            <td>${rack.part.kanban_id}</td>
                            <td>${rack.case_quantity}</td>
                        </tr>`;
                        tbody.append(row);

                    });
                });
            });
        }  
    };

    // 定期実行 
    setInterval(refreshPage, 1000);
    // setInterval(refreshPage, 5000); // TODO: testing
});

function goToDepallet(id) {

    const result = confirm(`間口 ${id}を呼び出します`);

    if (result) {
        $.ajax({
            url: "/line_frontage_click",
            type: "POST",
            contentType: "application/json",
            data: JSON.stringify({ "frontage_id": id }),
            success: function (data) {  
                console.log('Data >> Start() status' , data);
                if (data["status"] === "success") {
                        $.ajax({
                            url: "/to_maguchi_signal_input",
                            type: "POST",
                            contentType: "application/json",
                            data: JSON.stringify({ "line_frontage_id": id }),
                            success: function (data) {
                                console.log("to_maguchi_signal_input >> data >>", data);
                                $.ajax({
                                    url: "/to_maguchi_set_values",
                                    type: "POST",
                                    contentType: "application/json",
                                    data: JSON.stringify({ "line_frontage_id": id }),
                                    success: function (data) {
                                        console.log("to_maguchi_set_values >> data >>", data);
                                    },
                                    error: function (error) {
                                        alert("to_maguchi_set_values >> error");
                                    }
                                });
                            },
                            error: function (error) {
                                alert("to_maguchi_signal_input >> error");
                            }
                        });
                    setTimeout(() => {
                        $.ajax({
                            url: "/depallet",
                            type: "GET",
                            success: function (data) {
                                document.documentElement.innerHTML = data; // TODO: display depallet.html 
                            },
                            error: function (error) {
                                alert("error");
                            }
                        });
                    }, 500);

                } else {
                    alert("no flow racks");
                }
            },
            error: function (error) {
           
            }
        });
    } 
}