$(document).ready(function () {
 
    function refreshPage() {
    $.ajax({
        url: "/api/get_depallet_area_by_plat",
        type: "GET",
        success: function (data) {
            // console.log('get_depallet_area_by_plat >>', data); // TODO: testing
            // updateTable(data);
            getDepalletAreaByPlat(data);
        },
        error: function (error) {
            console.error("Error fetching data:", error);
        }
    });

    // TODO: comment out
    // function updateTable(data) {
    //     var depalletArea= JSON.parse(data);
    //     console.log('depalletArea >>', depalletArea);
    //     var frontages = depalletArea["frontages"];

    //     Object.keys(frontages).forEach((key,index) => {
    //         console.log('Key >> Index', key, index);

    //         let tbody = $(`#${index} tbody`);
                
    //         tbody.empty();
    //         let frontage = frontages[key];
    //         console.log('frontage >>', frontage);

    //         if (frontage.shelf == "None") {
    //             return;
    //         }
    //         if (frontage.shelf.type == 1) {
    //             Object.keys(frontage.shelf.inventories).forEach((key) => {

    //                 let tab =$(`#tab${index}`).contents().filter(function () {
    //                     console.log('contents >>,  nodeType >>', $(`#tab${index}`).contents(), this.nodeType);

    //                     return this.nodeType === 3;
    //                 }).first()

    //                 console.log('Tab >>>', tab);
    //                 tab.replaceWith(`間口${frontage.id}取出`);

    //                 tab.attr('data-id', `${frontage.id}`);  

    //                 let row = `
    //                 <tr>
    //                     <td><button onclick="Pallet(${frontage.id},'${frontage.shelf.inventories[key].part.kanban_id}')">＋</button></td>
    //                     <td>${frontage.shelf.inventories[key].part.kanban_id}</td>
    //                     <td>${frontage.shelf.inventories[key].case_quantity}</td>
    //                     <td><button onclick="Depallet(${frontage.id},'${frontage.shelf.inventories[key].part.kanban_id}')">ー</button></td>
    //                 </tr>`;
    //                 tbody.append(row);
    //             });
    //         }
    //      });
    // }; 
    // TODO: modified
    // function updateTable(data) {

    //     const depalletArea = JSON.parse(data);
    //     const frontages = depalletArea.frontages;

    //         Object.keys(frontages).forEach(key => {
    //             // console.log('frontages >> key >>', frontages, key)

    //             const frontage = frontages[key];
    //             console.log('frontage　>>', frontage)
                
    //             // shelf.type ==1 for kotatsu　、if kotatsu, it includes inventories array
                
    //             // これだけ追加（または修正）すれば完璧！
    //             const index = parseInt(key);   // ← ここが最重要！！ // TODO: confrim the key, hard code
    //             // console.log('frontage >> index >>', index)
        
    //             const tableId  = `shelf-${index}`;
    //             const tabLabelId = `tab${index}-tab`;
    //             const tbody  = $(`#${tableId} tbody`);
    //             const maguchiNoLabel = $('#maguchi-no');
    //             const kotatsuNoLabel = $('#kotatsu-no');

    //             const thead  = $(`#${tableId} thead`);

    //             // if (thead.length === 0) return;
    //             if (tbody.length === 0) return;
                
    //             if (frontage.shelf == "None") {
    //                 return
    //             }
    //             // console.log(`Shelf for frontage ${frontage.shelf.type}`);

    //             if (frontage.shelf.type == 1) {
    //                 $(`#${tabLabelId}`).html(`間口${frontage.id}`).addClass('btn-success');
    //                 maguchiNoLabel.text(`対象 : 間口 ${frontage.id}`);
    //                 kotatsuNoLabel.text(`コタツ No : ${frontage.id}`);
    //                 thead.empty();
    //                 tbody.empty();
    //                 const row1 = `
    //                         <th>　</th>
    //                         <th>背番号</th>
    //                         <th>在庫数</th>
    //                         <th>取出数量</th>
    //                         <th>　</th>`;
    //                 thead.append(row1);
    //                 // console.log('inventories >>', Object.values(frontage.shelf.inventories));
    //                 Object.values(frontage.shelf.inventories).forEach(inv => {
    //                     const row = `
    //                         <tr>
    //                             <td><button onclick="pallet(${frontage.id}, '${inv.part.kanban_id}')"><b>＋<b></button></td>
    //                             <td>背番号 ${inv.part.kanban_id}</td>
    //                             <td>背番号 ${inv.part.kanban_id}</td> <!-- load_num -->
    //                             <td>背番号 ${inv.part.kanban_id}</td> <!-- signal category -->
    //                             <!--  <td>${inv.case_quantity}</td> -->
    //                             <td><button onclick="depallet(${frontage.id}, '${inv.part.kanban_id}')"><b>ー</b></button></td>
    //                         </tr>`;
    //                     tbody.append(row);
    //                 });
    //             } else {
    //                 $(`#${tabLabelId}`).html(`間口${frontage.id}`).removeClass('btn-success');
    //                 // console.log('Coming here >>>');
    //                 // Reset display for all non-Type 2 shelves
    //                 // $(`#${tabLabelId}`).text(key).removeClass('btn-success'); TODO: comment out

    //                 // 未使用
    //                 thead.empty();
    //                 tbody.empty();
    //             }
    //         });
    // }
    
    
    // Track which maguchi IDs have data
    const maguchiHasData = {
        1: false,
        2: false,
        3: false,
        4: false,
        5: false
    };

    function getDepalletAreaByPlat(data) {

        const result = JSON.parse(data);

        // dummy
        // result = {
        //     "29": [{"step_kanban_no": "2006", "load_num": "0", "shelf_code": "K30147", "take_count": "-0", "flow_rack_no": "-0"}],
        //     "28": [{"step_kanban_no": "6001", "load_num": "0", "shelf_code": "K30144", "take_count": "-0", "flow_rack_no": "-0"}], 
        //     "24": [{"step_kanban_no": "3333", "load_num": "0", "shelf_code": "K30145", "take_count": "-0", "flow_rack_no": "378u30b5u30d6u2462"}],
        //     "23": [{"step_kanban_no": "T703", "load_num": "5", "shelf_code": "30007", "take_count": "-9", "flow_rack_no": "-0"}], 
        //     "21": [{"step_kanban_no": "u30aa070", "load_num": "40", "shelf_code": "30002", "take_count": "-1", "flow_rack_no": "-0"}]
        //  }
    
        // Map API keys to maguchi IDs
        const maguchiIdMap = {
            25: 1,
            26: 2,
            27: 3,
            28: 4,
            29: 5
        };

        
        // Reset flags
        Object.keys(maguchiHasData).forEach(id => maguchiHasData[id] = false);

        // Loop through key-value pairs
        Object.entries(result).forEach(([key, items]) => {
            const maguchiId = maguchiIdMap[key]; // Convert API key to 間口 ID
            if (!maguchiId) return; // Skip if not in map

            maguchiHasData[maguchiId] = true; // Mark this 間口 has data
    
            const tableId = `#shelf-${maguchiId}`;
            const tbody = $(`${tableId} tbody`);
            const thead = $(`${tableId} thead`);
            const maguchiNoLabel = $('#maguchi-no');
            const kotatsuNoLabel = $('#kotatsu-no');
            const kanbanNoLabel = $('#kanban-no');
    
            // Clear old content
            thead.empty();
            tbody.empty();
    
            // Add header
            thead.append(`
                <tr>
                    <th>プラス</th>
                    <th>背番号</th>
                    <th>在庫数</th>
                    <th>取出数量</th>
                    <th>ミネス</th>
                </tr>
            `);
    
            // Add rows
            items.forEach(item => {

                // Use Nullish Coalescing (??) for properties that might be missing or null
                const stepKanbanNo = item.step_kanban_no ?? 'N/A'; // Default for key
                const shelfCode = item.shelf_code ?? 'N/A';         // Default for key
                const loadNum = item.load_num ?? 0;                 // Default for numeric value
                const takeCount = item.take_count ?? 0;             // Default for numeric value
                const rowId = `row-${maguchiId}-${stepKanbanNo}`;

                maguchiNoLabel.text(`対象 : 間口 ${maguchiId}`);
                kotatsuNoLabel.text(`コタツ No : ${shelfCode}`);
                kanbanNoLabel.text(`かんばん No : ${stepKanbanNo}`);

               
    
                tbody.append(`
                    <tr id="${rowId}">
                        <td><button class="btn btn-success btn-sm" onclick="submitPallet(${maguchiId}, '${stepKanbanNo}')">＋</button></td>
                        <td>${stepKanbanNo}</td>
                        <td>${loadNum}</td>
                        <td id="take-count-${rowId}">${takeCount}</td>
                        <td><button class="btn btn-danger btn-sm" onclick="submitDepallet(${maguchiId}, '${stepKanbanNo}')">ー</button></td>
                    </tr>
                `);
            });
        });
    }
    
    // Hide/show title on tab click
    $('button[data-bs-toggle="tab"]').on('shown.bs.tab', function (e) {
        const targetId = $(e.target).attr('id'); // e.g., "tab3-tab"
        const maguchiId = parseInt(targetId.replace('tab', '').replace('-tab', '')); // Extract 1–5

        if (maguchiHasData[maguchiId]) {
            $('#display-title').show();
        } else {
            $('#display-title').hide();
        }
    });

    
    }
        // 定期実行 
        // setInterval(refreshPage, 500); // TODD

        
    $('#refreshButton').on('click', function () {
        refreshPage();
    });

});

    /**
     * Handles the click of the '+' button (Pallet/Increase takeCount)
     * @param {number} maguchiId - The ID of the shelf (maguchi)
     * @param {string} stepKanbanNo - The Kanban number identifying the item
     */
    function submitPallet(maguchiId, stepKanbanNo) {
        // 1. Determine the IDs for the row and the takeCount cell
        const rowId = `row-${maguchiId}-${stepKanbanNo}`;
        const takeCountCell = $(`#take-count-${rowId}`);
        
        // 2. Get the current value and calculate the new value
        let currentTakeCount = parseInt(takeCountCell.text().trim(), 10);
        let newTakeCount = currentTakeCount + 1; // No upper limit
        // Ensure we don't exceed the max value of 2
        // let newTakeCount = Math.min(currentTakeCount + 1, 2); 
        
        // 3. Send AJAX request to update the backend
        updateTakeCount(maguchiId, stepKanbanNo, newTakeCount, takeCountCell);
    }

    /**
     * Handles the click of the '-' button (Depallet/Decrease takeCount)
     * @param {number} maguchiId - The ID of the shelf (maguchi)
     * @param {string} stepKanbanNo - The Kanban number identifying the item
     */
    function submitDepallet(maguchiId, stepKanbanNo) {
        const rowId = `row-${maguchiId}-${stepKanbanNo}`;
        const takeCountCell = $(`#take-count-${rowId}`);

        // 2. Get the current value and calculate the new value
        let currentTakeCount = parseInt(takeCountCell.text().trim(), 10);
        let newTakeCount = currentTakeCount - 1; // No lower limit
        // Ensure we don't go below the min value of -2
        // let newTakeCount = Math.max(currentTakeCount - 1, -2);
        
        // 3. Send AJAX request to update the backend
        updateTakeCount(maguchiId, stepKanbanNo, newTakeCount, takeCountCell);
    }

    /**
     * Common function to handle the AJAX call and UI update.
     * @param {number} maguchiId 
     * @param {string} stepKanbanNo 
     * @param {number} newTakeCount 
     * @param {object} takeCountCell - The jQuery object for the <td> cell
     */

    function updateTakeCount(maguchiId, stepKanbanNo, newTakeCount, takeCountCell) {
        // Check if the number actually changed before hitting the API
        if (parseInt(takeCountCell.text().trim(), 10) === newTakeCount) {
            return; // No change, skip API call
        }

        $.ajax({
            url: "/api/update_take_count",
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({
                maguchi_id: maguchiId,
                kanban_no: stepKanbanNo,
                new_take_count: newTakeCount // ✅ Match Python key
            }),
            success: function(response) {
                if (response.status === "success") {
                    // Update UI only if backend confirms success
                    takeCountCell.text(newTakeCount);
                    showInfo("✅ Take count updated successfully!");
                    console.log("Take count updated successfully:", newTakeCount);
                } else {
                    // Backend returned error (e.g., kanban_no not found)
                    alert(response.message || "更新に失敗しました (Update failed).");
                    console.warn("Update failed:", response.message);
                }
            },
            error: function(xhr, status, error) {
                console.error("Error updating take count:", error);
                alert("サーバーエラーが発生しました (Server error occurred).");
            }
        });
    }


//パレットおろし
// function depallet(frontage_id,part_id) {
//     $.ajax({
//         url: "/api/to_flow_rack",
//         type: "POST",
//         contentType: "application/json",
//         data: JSON.stringify({ "frontage_id": frontage_id,"part_id" :part_id }),
//         success: function (data) {
//             if (data["status"] === "success") {
//                 console.log('depallet >> to_flow_rack API', "OK");
//             } else {
//                 alert("depalletizing error");
//             }
//         },
//         error: function (error) {
//             console.log('depallet >> to_flow_rack API >> Error', error.status + ": " + error.responseText);
//             alert(error.status + ": " + error.responseText)
//         }
//     });
// }

//パレット戻し, + plus
// function pallet(frontage_id, part_id) {
//     $.ajax({
//         url: "/api/to_kotatsu",
//         type: "POST",
//         contentType: "application/json",
//         data: JSON.stringify({ "frontage_id": frontage_id, "part_id": part_id }),
//         success: function (data) {
//             if (data["status"] === "success") {
//                 console.log('pallet >> to_kotatsu API', "OK");
//             } else {
//                 alert("palletizing error");
//             }
//         },
//         error: function (error) {
//             console.log('pallet >> to_kotatsu API >> Error', error.status + ">> " + error.responseText);
//             alert(error.status + ": " + error.responseText)
//         }
//     });
// }

// コタツ返却. - minus
function returnKotatsu(id) {
    // const frontage_id = element.getAttribute("data-id"); TODO: comment out
    console.log('returnKotatsu >>', id);
    const frontage_id = id;
    const result = confirm(`間口 ${frontage_id}のコタツを返却します`);

    if (result) {
        $.ajax({
            url: "/api/return_kotatsu",
            type: "POST",
            contentType: "application/json",
            data: JSON.stringify({ "frontage_id": frontage_id}),
            success: function (data) {
                if (data["status"] === "success") {
                    console.log('returnKotatsu API >>', "OK");
                } else {
                    alert("error");
                }
            },
            error: function (error) {
                console.log('returnKotatsu API >> Error', error);
                alert(error.status + ": " + error.responseText)
            }
        });
    }     
}
