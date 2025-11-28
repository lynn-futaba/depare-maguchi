$(document).ready(function () {
 
    function refreshPage() {
        $.ajax({
            url: "/api/update_product_info",
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

            let aProductRData = JSON.parse(data[0]); // TODO: add
            let aProductLData = JSON.parse(data[1]); // TODO: add
            let bProductRData = JSON.parse(data[2]); // TODO: add
            let bProductLData = JSON.parse(data[3]); // TODO: add
            let lineData = JSON.parse(data[4]);

            let tbodyAProduct = $('#a-product');
            let tbodyBProduct = $('#b-product');

            tbodyAProduct.empty();
            tbodyBProduct.empty();

            let displayAProduct = `
                <tr>
                    <td>${aProductRData.product.kanban_id}</td>
                    <td>${aProductRData.planned_num}</td>
                    <td>${aProductRData.output_num}</td>
                    <td>${aProductLData.product.kanban_id}</td>
                    <td>${aProductLData.planned_num}</td>
                    <td>${aProductLData.output_num}</td>
                </tr>
            `;
            tbodyAProduct.append(displayAProduct);

            let displayBProduct = `
                <tr>
                    <td>${bProductRData.product.kanban_id}</td>
                    <td>${bProductRData.planned_num}</td>
                    <td>${bProductRData.output_num}</td>
                    <td>${bProductLData.product.kanban_id}</td>
                    <td>${bProductLData.planned_num}</td>
                    <td>${bProductLData.output_num}</td>
                </tr>
            `;
            tbodyBProduct.append(displayBProduct);
          
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
    // setInterval(refreshPage, 1000); // TODO
    $('#refreshButton').on('click', function () {
        refreshPage();
    });
});

function callToBLINEAMR(id) {
    // TODO: to display 供給間口 
    const maguchiMap = {
        1: "Bライン(R1)", 2: "Bライン(R2)", 3: "Bライン(R3)", 4: "Bライン(L1)", 5: "Bライン(L2)", 6: "Bライン(L3)"
    };

    const kyokuuMaguchi = maguchiMap[id] || "不明"; // Default if id is invalid

    const result = confirm(`供給間口 ${kyokuuMaguchi}を呼び出します`);

    if (result) {
        $.ajax({
            url: "/api/line_frontage_click",
            type: "POST",
            contentType: "application/json",
            data: JSON.stringify({ "frontage_id": id }),
            success: function (data) {  
                console.log('Data >> Start() status' , data);
                if (data["status"] === "success") {
                        $.ajax({
                            url: "/api/insert_target_ids",
                            type: "POST",
                            contentType: "application/json",
                            data: JSON.stringify({ "line_frontage_id": id }),
                            success: function (data) {
                                console.log("insert_target_ids・間口に搬送対象idを入力 >> data >>", data);
                                alert("✅ 間口に搬送対象idを入力 完了しました!");
                                $.ajax({
                                    url: "/api/call_target_ids",
                                    type: "POST",
                                    contentType: "application/json",
                                    data: JSON.stringify({ "line_frontage_id": id }),
                                    success: function (data) {
                                        console.log("call_target_ids >> data >>", data);
                                        alert("✅ 間口に搬送対象を呼び出ました!");
                                        const nextPageUrl = `/depallet?id=${encodeURIComponent(id)}&name=${encodeURIComponent(kyokuuMaguchi)}`;
                                        window.open(nextPageUrl, "_blank"); // Opens new tab
                                    },
                                    error: function (error) {
                                        alert("❌　間口に搬送対象を呼び出せません");
                                    }
                                });
                            },
                            error: function (error) {
                                alert("❌ 間口に搬送対象idを入力出来ません", error);
                            }
                        });
                    // setTimeout(() => { // TODO: comment out
                        // $.ajax({
                        //     url: "/depallet",
                        //     type: "GET",
                        //     success: function (data) {
                        //         // document.documentElement.innerHTML = data; // TODO: display depallet.html 
                        //         const nextPageUrl = `/depallet.html?id=${encodeURIComponent(id)}`;
                        //         // Open in a new tab
                        //         window.open(nextPageUrl, "_blank");
                        //     },
                        //     error: function (error) {
                        //         alert("❌ Error loading depallet");
                        //     }
                        // });
                    // }, 500);
                } else {
                    alert("⚠️ No flow racks available");
                }
            },
            error: function (error) {
                alert("❌ Error in line_frontage_click");
            }
        });
    } 
}

function callToALINEAMR(id) {
    // TODO: to display 供給間口 
    const maguchiMap = {
        7: "Aライン R1", 8: "Aライン R2", 9: "Aライン R3", 10: "Aライン L1", 11: "Aライン L2", 12: "Aライン L3"
    };

    const kyokuuMaguchi = maguchiMap[id] || "不明 invalid ID"; // Default if id is invalid

    const result = confirm(`供給間口 ${kyokuuMaguchi}を呼び出します`);

    if (result) {
        $.ajax({
            url: "/api/line_frontage_click",
            type: "POST",
            contentType: "application/json",
            data: JSON.stringify({ "frontage_id": id }),
            success: function (data) {  
                console.log('Data >> Start() status' , data);
                if (data["status"] === "success") {
                        $.ajax({
                            url: "/api/insert_target_ids",
                            type: "POST",
                            contentType: "application/json",
                            data: JSON.stringify({ "line_frontage_id": id }),
                            success: function (data) {
                                console.log("insert_target_ids・間口に搬送対象idを入力 >> data >>", data);
                                alert("✅ 間口に搬送対象idを入力 完了しました!");
                                $.ajax({
                                    url: "/api/call_target_ids",
                                    type: "POST",
                                    contentType: "application/json",
                                    data: JSON.stringify({ "line_frontage_id": id }),
                                    success: function (data) {
                                        console.log("call_target_ids >> data >>", data);
                                        alert("✅ 間口に搬送対象を呼び出ました!");
                                        const nextPageUrl = `/depallet?id=${encodeURIComponent(id)}&name=${encodeURIComponent(kyokuuMaguchi)}`;
                                        window.open(nextPageUrl, "_blank"); // Opens new tab
                                    },
                                    error: function (error) {
                                        alert("❌　間口に搬送対象を呼び出せません", error);
                                    }
                                });
                            },
                            error: function (error) {
                                alert("❌ 間口に搬送対象idを入力出来ません");
                            }
                        });
                } else {
                    alert("⚠️ No flow racks available");
                }
            },
            error: function (error) {
                alert("❌ Error in line_frontage_click");
            }
        });
    } 
}
