$(document).ready(function () {
 
    function refreshPage() {

        getEmptyKotatsuStatus();
        // $.ajax({
        //     url: "/api/get_product_infos",
        //     type: "GET",
          
        //      success: function (data) {
        //         // console.log('get_product_infos >>', data); // TODO:
        //         updateProductInfo(data);
        //     },
        //     error: function (error) {
        //         console.error("Error fetching data:", error);
        //     }
        // });

        // function updateProductInfo(data) {

        //     let arProductData = JSON.parse(data[0]); // TODO: add
        //     let alProductLData = JSON.parse(data[1]); // TODO: add
        //     let brProductRData = JSON.parse(data[2]); // TODO: add
        //     let blProductLData = JSON.parse(data[3]); // TODO: add
        //     let lineData = JSON.parse(data[4]);

        //     let tbodyARProduct = $('#a-r-product');
        //     let tbodyALProduct = $('#a-l-product');

        //     let tbodyBRProduct = $('#b-r-product');
        //     let tbodyBLProduct = $('#b-l-product');

            

        //     tbodyARProduct.empty();
        //     tbodyALProduct.empty();
        //     tbodyBRProduct.empty();
        //     tbodyBLProduct.empty();

        //     let displayARProduct = `
        //         <tr>
        //             <td>${arProductData.product.kanban_id}</td>
        //             <td>${arProductData.planned_num}</td>
        //             <td>${arProductData.output_num}</td>
        //         </tr>
        //     `;
        //     tbodyARProduct.append(displayARProduct);

        //     let displayALProduct = `
        //         <tr>
        //             <td>${alProductLData.product.kanban_id}</td>
        //             <td>${alProductLData.planned_num}</td>
        //             <td>${alProductLData.output_num}</td>
        //         </tr>
        //     `;
        //     tbodyALProduct.append(displayALProduct);

        //     let displayBRProduct = `
        //         <tr>
        //             <td>${brProductRData.product.kanban_id}</td>
        //             <td>${brProductRData.planned_num}</td>
        //             <td>${brProductRData.output_num}</td>
        //         </tr>
        //     `;
        //     tbodyBRProduct.append(displayBRProduct);

        //     let displayBLProduct = `
        //         <tr>
        //             <td>${blProductLData.product.kanban_id}</td>
        //             <td>${blProductLData.planned_num}</td>
        //             <td>${blProductLData.output_num}</td>
        //         </tr>
        //     `;
        //     tbodyBLProduct.append(displayBLProduct);


          
        //     Object.keys(lineData).forEach((key) => {

        //         let line = lineData[key]
        //         // TODO: current frontages is {}, need to ask for testing
        //         Object.keys(line.frontages).forEach((key) => {
                   
        //             let frontage = line.frontages[key];
        //             let tbody = $(`#${frontage.id}`);
        //             tbody.empty();

        //             Object.keys(frontage.inventories).forEach((key) => {
        //                 let rack = frontage.inventories[key];
                                          
        //                 let row = `
        //                 <tr>
        //                     <td>${rack.part.kanban_id}</td>
        //                     <td>${rack.case_quantity}</td>
        //                 </tr>`;
        //                 tbody.append(row);

        //             });
        //         });
        //     });
        // }  
    };

    // 定期実行 TODO: comment out
    setInterval(refreshPage, 3000); // TODO
    $('#refreshButton').on('click', function () {
        refreshPage();
    });
});

// TODO: GET Empty Kotatsu Status
function getEmptyKotatsuStatus() {
    $.ajax({
        url: "/api/get_empty_kotatsu_status",
        type: "GET",
        success: function (data) {
            const $alertContainer = $("#kotatsu-alert");
            const $leftList = $("#left-list");
            const $rightList = $("#right-list");

            if (data.status === "success" && data.suppliers && data.suppliers.length > 0) {
                // Clear old data
                $leftList.empty();
                $rightList.empty();

                let leftCounter = 0;
                let rightCounter = 0;

                data.suppliers.forEach(function(name) {
                    // 1. Determine side based on supplier_name
                    // Assumes names like "Supplier-L" or "L-Supplier"
                    let side = "";
                    if (name.includes("L")) side = "L";
                    else if (name.includes("R")) side = "R";

                    // 2. Determine if it is the first item for that specific side
                    let isFirstForSide = false;
                    if (side === "L") {
                        isFirstForSide = (leftCounter === 0);
                        leftCounter++;
                    } else if (side === "R") {
                        isFirstForSide = (rightCounter === 0);
                        rightCounter++;
                    }

                    // 3. Create HTML
                    let label = isFirstForSide ? '<span class="text-primary">Next ➞ </span>' : '・';
                    let html = '<div class="border-bottom py-2">' + label + name + ' が空です。</div>';

                    // 4. Append to the correct side
                    if (side === "L") {
                        $leftList.append(html);
                    } else if (side === "R") {
                        $rightList.append(html);
                    }
                });

                // Show alert only if at least one side has content
                if (leftCounter > 0 || rightCounter > 0) {
                    $alertContainer.removeClass("d-none");
                } else {
                    $alertContainer.addClass("d-none");
                }
            } else {
                $alertContainer.addClass("d-none");
            }
        },
        error: function (error) {
            $("#kotatsu-alert").addClass("d-none");
            console.error("AJAX Error:", error);
        }
    });
}

// TODO: call to B LINE Depallet Maguchi
function callToBLineDepalletMaguchi(id) {
    // TODO: to display 供給間口 
    const maguchiMap = {
        // 1: "Bライン(R1)", 2: "Bライン(R2)", 3: "Bライン(R3)", 4: "Bライン(L1)", 5: "Bライン(L2)", 6: "Bライン(L3)"
        1: "(R1)", 2: "(R2)", 3: "(R3)", 4: "(L1)", 5: "(L2)", 6: "(L3)"

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
                            data: JSON.stringify({ "button_id": id }),
                            success: function (data) {
                                console.log("insert_target_ids・間口に搬送対象idを入力 >> data >>", data);
                                // showInfo("✅ Bライン ➞ 間口に搬送対象idを入力 完了しました!");
                                showInfo("✅ 間口に搬送対象idを入力 完了しました!");
                                $.ajax({
                                    url: "/api/call_target_ids",
                                    type: "POST",
                                    contentType: "application/json",
                                    data: JSON.stringify({ "button_id": id }),
                                    success: function (data) {
                                        console.log("call_target_ids >> data >>", data);
                                        // showInfo("✅ Bライン ➞ 間口に搬送対象を呼び出ました!");
                                        showInfo("✅ 間口に搬送対象を呼び出ました!");
                                        // const nextPageUrl = `/b_line_depallet_maguchi?id=${encodeURIComponent(id)}&name=${encodeURIComponent(kyokuuMaguchi)}`;
                                        // window.open(nextPageUrl, "_blank"); // Opens new tab

                                        // Combine id and name to create a unique reference for the window
                                        const windowIdentifier = `maguchi_${id}_${kyokuuMaguchi}`;

                                        const nextPageUrl = `/b_line_depallet_maguchi?id=${encodeURIComponent(id)}&name=${encodeURIComponent(kyokuuMaguchi)}`;

                                        // Providing 'windowIdentifier' instead of '_blank' tells the browser 
                                        // to reuse the tab if it is already open.
                                        const openedWindow = window.open(nextPageUrl, windowIdentifier);

                                        // This ensures the existing tab is brought to the front (focused) if it was already open
                                        if (openedWindow) {
                                            openedWindow.focus();
                                        }

                                    },
                                    error: function (error) {
                                        showInfo("❌ Bライン ➞ 間口に搬送対象を呼び出せません");
                                    }
                                });
                            },
                            error: function (error) {
                                showInfo("❌ Bライン ➞ 間口に搬送対象idを入力出来ません", error);
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


// // TODO: call to A LINE Depallet Maguchi
// function callToALineDepalletMaguchi(id) {
//     // TODO: to display 供給間口 
//     const maguchiMap = {
//         7: "Aライン(R1)", 8: "Aライン(R2)", 9: "Aライン(R3)", 10: "Aライン(L1)", 11: "Aライン(L2)", 12: "Aライン(L3)"
//     };

//     const kyokuuMaguchi = maguchiMap[id] || "不明 invalid ID"; // Default if id is invalid

//     const result = confirm(`供給間口 ${kyokuuMaguchi}を呼び出します`);

//     if (result) {
//         $.ajax({
//             url: "/api/line_frontage_click",
//             type: "POST",
//             contentType: "application/json",
//             data: JSON.stringify({ "frontage_id": id }),
//             success: function (data) {  
//                 console.log('Data >> Start() status' , data);
//                 if (data["status"] === "success") {
//                         $.ajax({
//                             url: "/api/insert_target_ids",
//                             type: "POST",
//                             contentType: "application/json",
//                             data: JSON.stringify({ "button_id": id }),
//                             success: function (data) {
//                                 console.log("insert_target_ids・間口に搬送対象idを入力 >> data >>", data);
//                                 showInfo("✅ 間口に搬送対象idを入力 完了しました!");
//                                 $.ajax({
//                                     url: "/api/call_target_ids",
//                                     type: "POST",
//                                     contentType: "application/json",
//                                     data: JSON.stringify({ "button_id": id }),
//                                     success: function (data) {
//                                         console.log("call_target_ids >> data >>", data);
//                                         showInfo("✅ Aライン ➞ 間口に搬送対象を呼び出ました!");
//                                         const nextPageUrl = `/a_line_depallet_maguchi?id=${encodeURIComponent(id)}&name=${encodeURIComponent(kyokuuMaguchi)}`;
//                                         window.open(nextPageUrl, "_blank"); // Opens new tab
//                                     },
//                                     error: function (error) {
//                                         showInfo("❌Aライン ➞間口に搬送対象を呼び出せません", error);
//                                     }
//                                 });
//                             },
//                             error: function (error) {
//                                 showInfo("❌ 間口に搬送対象idを入力出来ません");
//                             }
//                         });
//                 } else {
//                     alert("⚠️ No flow racks available");
//                 }
//             },
//             error: function (error) {
//                 alert("❌ Error in line_frontage_click");
//             }
//         });
//     } 
// }

// TODO: かんばん抜きの発進を呼び出し
function submitKanbanNuki() {
    $.ajax({
        url: "/api/insert_kanban_nuki",
        type: "GET",
        contentType: "application/json",
        success: function (data) {
            console.log("insert_kanban_nuki >> data >>", data);
            alert("✅ かんばん抜きの発進を呼び出ました!");
        },
        error: function (error) {
            alert("❌ かんばん抜きの発進を呼び出せません", error);
        }
    });
}

// TODO: かんばん差しの発進を呼び出し
function submitKanbanSashi() {
    $.ajax({
        url: "/api/insert_kanban_sashi",
        type: "GET",
        contentType: "application/json",
        success: function (data) {
            console.log("insert_kanban_sashi >> data >>", data);
            alert("✅ かんばん差しの発進を呼び出ました!");
        },
        error: function (error) {
            alert("❌ かんばん差しの発進を呼び出せません", error);
        }
    });
}

// TODO: かんばん呼び出しの発進を呼び出し
function submitKanbanYobiDashi() {
    $.ajax({
        url: "/api/insert_kanban_yobi_dashi",
        type: "GET",
        contentType: "application/json",
        success: function (data) {
            console.log("insert_kanban_yobi_dashi >> data >>", data);
            alert("✅ かんばん呼び出しの発進を呼び出ました!");
        },
        error: function (error) {
            alert("❌ かんばん呼び出しの発進を呼び出せません", error);
        }
    });
}
