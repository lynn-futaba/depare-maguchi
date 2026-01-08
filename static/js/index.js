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
// function callToBLineDepalletMaguchi(id) {
//     // TODO: to display 供給間口 
//     const maguchiMap = {
//         // 1: "Bライン(R1)", 2: "Bライン(R2)", 3: "Bライン(R3)", 4: "Bライン(L1)", 5: "Bライン(L2)", 6: "Bライン(L3)"
//         1: "R1", 2: "R2", 3: "R3", 4: "L1", 5: "L2", 6: "L3"

//     };

//     const kyokuuMaguchi = maguchiMap[id] || "不明"; // Default if id is invalid

//     const result = confirm(`供給間口 ${kyokuuMaguchi}を呼び出します`);

//     if (result) {
//         // STEP 1: Click the frontage
//         $.ajax({
//             url: "/api/line_frontage_click",
//             type: "POST",
//             contentType: "application/json",
//             data: JSON.stringify({ "frontage_id": id }),
//             success: function (data) {  
//                 console.log('Data >> Start() status' , data);
//                 if (data["status"] === "success") {

//                     // --- NEW CHECK START ---
//                     // STEP 2: Check Kotatsu status BEFORE inserting IDs
//                     $.ajax({
//                         url: "/api/get_fill_kotatsu_status",
//                         type: "GET",
//                         success: function (kotatsuData) {
//                             let fullMessage = "";

//                             if (kotatsuData.status === "empty") {
//                                 // CASE: FILL exists. Message: "⚠️ 現在搬送中です。"
//                                 fullMessage = `⚠️ 現在 ${kotatsuData.message}`; 
//                             } else {
//                                 // CASE: No FILL. Message: "T621 が無いです...\n呼び出しますか ?"
//                                 let kanbanMessage = "";
//                                 if (kotatsuData.kanban_list && kotatsuData.kanban_list.length > 0) {
//                                     kanbanMessage = kotatsuData.kanban_list.map(no => `${no} が無いです。`).join("\n");
//                                 }
//                                 fullMessage = `${kanbanMessage}\n\n${kotatsuData.message}`;
//                             }

//                             // The ONLY gate to continue to Insert logic
//                             const proceed = confirm(fullMessage);
                    
//                             if (proceed) {
//                                 console.log("User confirmed. Proceeding to insert IDs.");
//                                 triggerBuhinCallSteps();      
//                             } else {
//                                 console.log("User cancelled the triggerBuhinCallSteps().");
//                             }
//                         }
//                     });
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

// function triggerBuhinCallSteps() {
//      // STEP 3: Insert IDs logic
//      $.ajax({
//         url: "/api/insert_target_ids",
//         type: "POST",
//         contentType: "application/json",
//         data: JSON.stringify({ "button_id": id }),
//         success: function (data) {
//             console.log("insert_target_ids・間口に搬送対象idを入力 >> data >>", data);
//             // showInfo("✅ Bライン ➞ 間口に搬送対象idを入力 完了しました!");
//             showInfo("✅ 間口に搬送対象idを入力 完了しました!");
//             $.ajax({　// STEP 4: Call target IDs
//                 url: "/api/call_target_ids",
//                 type: "POST",
//                 contentType: "application/json",
//                 data: JSON.stringify({ "button_id": id }),
//                 success: function (data) {
//                     console.log("call_target_ids >> data >>", data);
//                     // showInfo("✅ Bライン ➞ 間口に搬送対象を呼び出ました!");
//                     showInfo("✅ 間口に搬送対象を呼び出ました!");

//                     // Combine id and name to create a unique reference for the window
//                     const windowIdentifier = `maguchi_${id}_${kyokuuMaguchi}`;
//                     const nextPageUrl = `/b_line_depallet_maguchi?id=${encodeURIComponent(id)}&name=${encodeURIComponent(kyokuuMaguchi)}`;

//                     // Providing 'windowIdentifier' instead of '_blank' tells the browser 
//                     // to reuse the tab if it is already open.
//                     const openedWindow = window.open(nextPageUrl, windowIdentifier);

//                     // This ensures the existing tab is brought to the front (focused) if it was already open
//                     if (openedWindow) {
//                         openedWindow.focus();
//                     }

//                 },
//                 error: function (error) {
//                     showInfo("❌ 間口に搬送対象を呼び出せません");
//                 }
//             });
//         },
//         error: function (error) {
//             showInfo("❌ 間口に搬送対象idを入力出来ません", error);
//         }
//     });
// }

function callToBLineDepalletMaguchi(id) {
    const maguchiMap = { 1: "R1", 2: "R2", 3: "R3", 4: "L1", 5: "L2", 6: "L3" };
    const kyokuuMaguchi = maguchiMap[id] || "不明";

    // Step 1: Initial Confirmation
    if (confirm(`供給間口 ${kyokuuMaguchi}を呼び出します。よろしいですか？`)) {
        $.ajax({
            url: "/api/line_frontage_click",
            type: "POST",
            contentType: "application/json",
            data: JSON.stringify({ "frontage_id": id }),
            success: function (data) {
                if (data["status"] === "success") {
                    
                    // Step 2: Check AMR/Kotatsu Status (Logic preserved)
                    $.ajax({
                        url: "/api/get_fill_kotatsu_status",
                        type: "GET",
                        success: function (kotatsuData) {
                            if (kotatsuData.status === "empty") {
                                // CASE: BUSY
                                let statusMsg =  `⚠️ 現在${kotatsuData.message}`;

                            if (confirm(statusMsg)) {
                                // Start the process and pass a "UI handle" to remove later
                                startWorkSequence(id, kyokuuMaguchi, statusMsg);
                            }                            
                        } 
                            
                            else {
                                // CASE: IDLE
                                let kanbanMessage = kotatsuData.kanban_list?.map(no => `${no} が無いです。`).join("\n") || "";
                                if (confirm(`${kanbanMessage}\n\n${kotatsuData.message}`)) {
                                    processStartSequence(id, kyokuuMaguchi, "搬送指示を送信中...");
                                }
                            }
                        }
                    });
                }
            }
        });
    }
}

function startWorkSequence(id, kyokuuMaguchi, message) {
    // 1. Create a unique ID for this specific process "child" element
    const processId = "proc_" + new Date().getTime();
    
    // 2. Open Maguchi Window immediately
    const nextPageUrl = `/b_line_depallet_maguchi?id=${id}&name=${kyokuuMaguchi}`;
    const childWin = window.open(nextPageUrl, `win_${id}`);

    // 3. Show a "Processing Card" instead of an overlay
    // This adds a small, fixed notification box that we can easily .remove()
    const statusHtml = `
        <div id="${processId}" class="alert alert-warning shadow-lg" 
             style="position: fixed; bottom: 20px; right: 20px; z-index: 9999; min-width: 300px;">
            <div class="d-flex align-items-center">
                <div class="spinner-border spinner-border-sm me-3"></div>
                <strong>${kyokuuMaguchi}: ${message}</strong>
            </div>
        </div>`;
    $('body').append(statusHtml);

    // 4. Run the backend chain
    triggerBuhinCallStepsOther(id, processId, childWin);
}

function triggerBuhinCallStepsOther(id, elementId, childWin) {
    $.ajax({
        url: "/api/insert_target_ids",
        type: "POST",
        contentType: "application/json",
        data: JSON.stringify({ "button_id": id }),
        success: function () {
            $.ajax({
                url: "/api/call_target_ids",
                type: "POST",
                contentType: "application/json",
                data: JSON.stringify({ "button_id": id }),
                timeout: 65000, 
                success: function (response) {
                    // --- REMOVE THE CHILD ELEMENT EASILY ---
                    $(`#${elementId}`).remove(); 

                    if (response.processing_status === "completed") {
                        showInfo("✅ 搬送開始を確認しました！");
                        if (childWin) childWin.focus();
                    }
                },
                error: function () {
                    $(`#${elementId}`).remove();
                    showInfo("エラーが発生しました。");
                }
            });
        }
    });
}
// Logic to open child window and start background monitoring
function processStartSequence(id, kyokuuMaguchi, initialMsg) {

    showInfo(initialMsg, 50000);

    // 1. Open the Maguchi page immediately (Child Window)
    const windowIdentifier = `maguchi_${id}_${kyokuuMaguchi}`;
    const nextPageUrl = `/b_line_depallet_maguchi?id=${encodeURIComponent(id)}&name=${encodeURIComponent(kyokuuMaguchi)}`;
    const openedWindow = window.open(nextPageUrl, windowIdentifier);

    // 2. Start the backend call chain
    triggerBuhinCallSteps(id, openedWindow);
}

function triggerBuhinCallSteps(id, childWindow) {
    $.ajax({
        url: "/api/insert_target_ids",
        type: "POST",
        contentType: "application/json",
        data: JSON.stringify({ "button_id": id }),
        success: function () {
            showInfo("AMRの応答を待機中...", 5000);

            // Long-polling call: waits for using_flag == 1 in the backend
            $.ajax({
                url: "/api/call_target_ids",
                type: "POST",
                contentType: "application/json",
                data: JSON.stringify({ "button_id": id }),
                timeout: 60000, 
                success: function (response) {
                    if (response.processing_status === "completed") {
                        // Success Toast
                        showInfo("✅ 搬送開始を確認しました！", 3000);
                        
                        // Focus the newly opened tab if possible
                        if (childWindow && !childWindow.closed) {
                            childWindow.focus();
                        }
                    } else {
                        showInfo("タイムアウト: AMRの反応がありません。");
                    }
                },
                error: function () {
                    showInfo("搬送呼び出し中にエラーが発生しました。");
                }
            });
        },
        error: function () {
            showInfo("データの登録に失敗しました。");
        }
    });
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
