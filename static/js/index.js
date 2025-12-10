$(document).ready(function () {
 
    function refreshPage() {
        $.ajax({
            url: "/api/get_product_infos",
            type: "GET",
          
             success: function (data) {
                // console.log('get_product_infos >>', data); // TODO:
                updateProductInfo(data);
            },
            error: function (error) {
                console.error("Error fetching data:", error);
            }
        });

        function updateProductInfo(data) {

            let arProductData = JSON.parse(data[0]); // TODO: add
            let alProductLData = JSON.parse(data[1]); // TODO: add
            let brProductRData = JSON.parse(data[2]); // TODO: add
            let blProductLData = JSON.parse(data[3]); // TODO: add
            let lineData = JSON.parse(data[4]);

            let tbodyARProduct = $('#a-r-product');
            let tbodyALProduct = $('#a-l-product');

            let tbodyBRProduct = $('#b-r-product');
            let tbodyBLProduct = $('#b-l-product');

            

            tbodyARProduct.empty();
            tbodyALProduct.empty();
            tbodyBRProduct.empty();
            tbodyBLProduct.empty();

            let displayARProduct = `
                <tr>
                    <td>${arProductData.product.kanban_id}</td>
                    <td>${arProductData.planned_num}</td>
                    <td>${arProductData.output_num}</td>
                </tr>
            `;
            tbodyARProduct.append(displayARProduct);

            let displayALProduct = `
                <tr>
                    <td>${alProductLData.product.kanban_id}</td>
                    <td>${alProductLData.planned_num}</td>
                    <td>${alProductLData.output_num}</td>
                </tr>
            `;
            tbodyALProduct.append(displayALProduct);

            let displayBRProduct = `
                <tr>
                    <td>${brProductRData.product.kanban_id}</td>
                    <td>${brProductRData.planned_num}</td>
                    <td>${brProductRData.output_num}</td>
                </tr>
            `;
            tbodyBRProduct.append(displayBRProduct);

            let displayBLProduct = `
                <tr>
                    <td>${blProductLData.product.kanban_id}</td>
                    <td>${blProductLData.planned_num}</td>
                    <td>${blProductLData.output_num}</td>
                </tr>
            `;
            tbodyBLProduct.append(displayBLProduct);


          
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
    // setInterval(refreshPage, 5000); // TODO
    $('#refreshButton').on('click', function () {
        refreshPage();
    });
});

// TODO: call to B LINE Depallet Maguchi
function callToBLineDepalletMaguchi(id) {
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
                                showInfo("✅ 間口に搬送対象idを入力 完了しました!");
                                $.ajax({
                                    url: "/api/call_target_ids",
                                    type: "POST",
                                    contentType: "application/json",
                                    data: JSON.stringify({ "line_frontage_id": id }),
                                    success: function (data) {
                                        console.log("call_target_ids >> data >>", data);
                                        showInfo("✅ 間口に搬送対象を呼び出ました!");
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


// TODO: call to A LINE Depallet Maguchi
function callToALineDepalletMaguchi(id) {
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
                                showInfo("✅ 間口に搬送対象idを入力 完了しました!");
                                $.ajax({
                                    url: "/api/call_target_ids",
                                    type: "POST",
                                    contentType: "application/json",
                                    data: JSON.stringify({ "line_frontage_id": id }),
                                    success: function (data) {
                                        console.log("call_target_ids >> data >>", data);
                                        showInfo("✅ 間口に搬送対象を呼び出ました!");
                                        const nextPageUrl = `/a_line_depallet_maguchi?id=${encodeURIComponent(id)}&name=${encodeURIComponent(kyokuuMaguchi)}`;
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

// TODO: かんばん抜きの発信を呼び出し
function submitKanbanNuki() {
    $.ajax({
        url: "/api/insert_kanban_nuki",
        type: "GET",
        contentType: "application/json",
        success: function (data) {
            console.log("insert_kanban_nuki >> data >>", data);
            alert("✅ かんばん抜きの発信を呼び出ました!");
        },
        error: function (error) {
            alert("❌ かんばん抜きの発信を呼び出せません", error);
        }
    });
}

// TODO: かんばん差しの発信を呼び出し
function submitKanbanSashi() {
    $.ajax({
        url: "/api/insert_kanban_sashi",
        type: "GET",
        contentType: "application/json",
        success: function (data) {
            console.log("insert_kanban_sashi >> data >>", data);
            alert("✅ かんばん差しの発信を呼び出ました!");
        },
        error: function (error) {
            alert("❌ かんばん差しの発信を呼び出せません", error);
        }
    });
}
