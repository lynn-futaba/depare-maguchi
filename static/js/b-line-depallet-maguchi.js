let getAMRDataStorage = {}
// ⭐ Define a global variable to hold the timer ID
let pageRefreshIntervalId;

$(document).ready(function () {
 
    function refreshPage() {
        console.log("Page refreshed automatically.");
        const params = new URLSearchParams(window.location.search);
        const idValue = parseInt(params.get("id"));
        const nameValue = params.get("name");

        if (nameValue.includes("L")) {
            document.getElementById("layout-L").style.display = "block";
        } else {
            document.getElementById("layout-normal").style.display = "block";
        }

        $.ajax({
            url: "/api/get_depallet_area_by_plat",
            type: "POST",
            contentType: 'application/json',
            // data: JSON.stringify({
            //     button_id: idValue 
            // }),
            success: function (data) {
                // console.log('get_depallet_area_by_plat >>', data); // TODO: testing
                // updateTable(data);
                getDepalletAreaByPlat(data, idValue, nameValue);
                console.log('1st getAMR DataStorage', getAMRDataStorage);

                // Save data in localStorage
                localStorage.setItem("getAMRDataStorage", JSON.stringify(data));

                // For debugging
                console.log('Data saved to localStorage:', data);            
            },
            error: function (error) {
                console.error("Error fetching data:", error);
            }
        });

    
        // function getDepalletAreaByPlat(data, idValue, nameValue) {

        //     const result = JSON.parse(data);

        //     // Button → Plat mapping
        //     const buttonIdMap = { 
        //         1: [29, 28, 27, 26], // R1, Bライン
        //         2: [29, 28, 27, 26], // R2, Bライン
        //         3: [28,27],         // R3, Bライン
        //         4: [28, 27, 26, 25], // L1, Bライン
        //         5: [28, 27, 26, 25], // L2, Bライン
        //         6: [27, 26],         // L3, Bライン
        //     };

        //     const targetPlats = buttonIdMap[idValue] || [];
        //     document.getElementById("frontageName").textContent = 'デパレ間口 <' + nameValue + '>';

        //     // ✅ Loop through shelves in reverse order (4 → 1)
        //     for (let i = 4; i >= 1; i--) {
        //         const shelfId = `#shelf-${i}`; // shelf-4, shelf-3, shelf-2, shelf-1
        //         // const cardBody = $(shelfId).closest('.card-body');
        //         const tbody = $(`${shelfId} tbody`);
        //         const thead = $(`${shelfId} thead`);

        //         let cardId = `#card${i}`;
        //         let cardNo = $(`${cardId} tbody`);

        //         // cardBody.find('.dynamic-labels').remove();
        //         thead.empty();
        //         tbody.empty();
        //         cardNo.empty();
                

        //         const platId = targetPlats[4 - i]; // Map correctly to buttonIdMap array
        //         const items = result[platId] || [];

        //         if (items.length > 0) {
        //             // ✅ Add table header
        //             thead.append(`
        //                 <tr>
        //                     <th>対象 : 間口${i}</th>
        //                     <th colspan="2">コタツ No : ${items[0]?.shelf_code || 'N/A'}</th>
        //                     <th colspan="2">かんばん No : ${items[0]?.step_kanban_no || 'N/A'}</th>
        //                 </tr>
        //                 <tr>
        //                     <th></th>
        //                     <th>背番号</th>
        //                     <th>在庫数</th>
        //                     <th>取出数量</th>
        //                     <th></th>
        //                 </tr>
        //             `);

        //             // ✅ Populate rows
        //             items.forEach((item, idx) => {
        //                 const stepKanbanNo = item.step_kanban_no || '-';
        //                 const loadNum = item.load_num || 0;
        //                 const takeCount = item.take_count || 0;
        //                 const rowId = `row-${platId}-${stepKanbanNo}` || '-';

        //                 // Update flow rack info
        //                 const flowRackNo = item.flow_rack_no ?? '-';
        //                 $("#flow-rack-no").text(`対象フローラック No: ${flowRackNo}`);

                        
        //                 // <td><button class="btn btn-success btn-sm" onclick="submitPallet(${platId}, '${stepKanbanNo}')">＋</button></td>
        //                 // <td><button class="btn btn-danger btn-sm" onclick="submitDepallet(${platId}, '${stepKanbanNo}')">ー</button></td>
        //                 // Add row to shelf table
        //                 tbody.append(`
        //                     <tr id="${rowId}">
        //                         <td><button class="btn btn-success btn-sm submit-pallet" data-plat="${platId}" data-kanban="${stepKanbanNo}">＋</button></td>
        //                         <td>${stepKanbanNo}</td>
        //                         <td>${loadNum}</td>
        //                         <td id="take-count-${rowId}">${takeCount}</td>
        //                         <td><button class="btn btn-danger btn-sm submit-depallet" data-plat="${platId}" data-kanban="${stepKanbanNo}">ー</button></td>
        //                     </tr>
        //                 `);
                        
        //                 cardNo.append(`
        //                     <tr id="${rowId}">
        //                         <td>${stepKanbanNo}</td>
        //                         <td id="take-count-${rowId}">${takeCount}</td>
        //                     </tr>
        //                 `);  
        //             });
        //         } else {
        //             // Add the "No data" row to the table body
        //             tbody.append(`
        //                 <tr>
        //                     <td colspan="5" class="p-3 text-danger">
        //                         データが見つかりません
        //                     </td>
        //                 </tr>
        //             `);
        //             cardNo.append(`
        //                 <tr>
        //                     <td colspan="5" class="text-danger">
        //                         データが見つかりません
        //                     </td>
        //                 </tr>
        //             `);  
        //         }
        //     }
        // }

        function getDepalletAreaByPlat(data, idValue, nameValue) {

            const result = JSON.parse(data);

            // 1. Button → Plat (Data Source) mapping
            const buttonIdMap = { 
                1: [29, 28, 27, 26], // R1, Bライン, 間口[5,4,3,2]
                2: [29, 28, 27, 26], // R2, Bライン, 間口[5,4,3,2]
                3: [28, 27],         // R3, Bライン, 間口[4,3]
                4: [28, 27, 26, 25],// L1, Bライン, 間口[4,3,2,1]
                5: [28, 27, 26, 25],// L2, Bライン, 間口[4,3,2,1]
                6: [27, 26]         // L3, Bライン, 間口[3,2]
            };

            // 2. Button → Shelf IDs (Display UI) mapping
            const shelfMap = {
                1:  [5, 4, 3, 2], 
                2:  [5, 4, 3, 2],
                3:  [4, 3],
                4: [4, 3, 2, 1],
                5: [4, 3, 2, 1],
                6: [3, 2]
            };

            const targetPlats = buttonIdMap[idValue] || [];
            const targetShelves = shelfMap[idValue] || [];

            document.getElementById("frontageName").textContent = 'デパレ間口 <' + nameValue + '>';

            // First, clear ALL possible shelves (1-5) to avoid ghost data from previous clicks
            for (let i = 1; i <= 5; i++) {
                $(`#shelf-${i} thead, #shelf-${i} tbody, #card${i} tbody`).empty();
            }

            // ✅ Dynamic Loop based on the targetShelves array
            // shelfIndex helps pick the correct platId from the buttonIdMap
            targetShelves.forEach((shelfNum, shelfIndex) => {

                const shelfId = `#shelf-${shelfNum}`; // shelf-4, shelf-3, shelf-2, shelf-1
                // const cardBody = $(shelfId).closest('.card-body');
                const tbody = $(`${shelfId} tbody`);
                const thead = $(`${shelfId} thead`);

                let cardId = `#card${shelfNum}`;
                let cardNo = $(`${cardId} tbody`);

                // cardBody.find('.dynamic-labels').remove();
                thead.empty();
                tbody.empty();
                cardNo.empty();
                

                const platId = targetPlats[shelfIndex]; // Map correctly to buttonIdMap array
                const items = result[platId] || [];

                if (items && items.length > 0) {
                    // ✅ Add table header
                    thead.append(`
                        <tr>
                            <th>対象 : 間口${shelfNum}</th>
                            <th colspan="2">コタツ No : ${items[0]?.shelf_code ?? 'N/A'}</th>
                            <th colspan="2">かんばん No : ${items[0]?.step_kanban_no ?? 'N/A'}</th>
                        </tr>
                        <tr>
                            <th></th>
                            <th>背番号</th>
                            <th>在庫数</th>
                            <th>取出数量</th>
                            <th></th>
                        </tr>
                    `);

                    // ✅ Populate rows
                    items.forEach((item, idx) => {
                        const stepKanbanNo = item.step_kanban_no ?? '-';
                        const loadNum = item.load_num ?? 0;
                        const takeCount = item.take_count ?? 0;
                        const rowId = `row-${platId}-${stepKanbanNo}`;

                        // Update flow rack info
                        const flowRackNo = item.flow_rack_no ?? '-';
                        $("#flow-rack-no").text(`対象フローラック No:${flowRackNo}`);

                        // Add row to shelf table
                        tbody.append(`
                            <tr id="${rowId}">
                                <td><button class="btn btn-success btn-sm submit-pallet" data-plat="${platId}" data-kanban="${stepKanbanNo}">＋</button></td>
                                <td>${stepKanbanNo}</td>
                                <td>${loadNum}</td>
                                <td id="take-count-${rowId}">${takeCount}</td>
                                <td><button class="btn btn-danger btn-sm submit-depallet" data-plat="${platId}" data-kanban="${stepKanbanNo}">ー</button></td>
                            </tr>
                        `);
                        
                        cardNo.append(`
                            <tr id="${rowId}">
                                <td>${stepKanbanNo}</td>
                                <td id="take-count-${rowId}">${takeCount}</td>
                            </tr>
                        `);  
                    });
                } else {
                    // ✅ Show "No data" message specifically for this shelf-id
                    tbody.append(`
                        <tr>
                            <td colspan="5" class="p-3 text-danger text-center">
                                間口${shelfNum}: データが見つかりません
                            </td>
                        </tr>
                    `);
                    cardNo.append(`
                        <tr>
                            <td colspan="2" class="text-danger text-center">
                                データなし
                            </td>
                        </tr>
                    `); 
                }
            });
        }

    }

    // Attach event handler for '+' button clicks (submitPallet logic)
    $(document).on('click', '.submit-pallet', function() {
        const maguchiId = $(this).data('plat');
        const stepKanbanNo = $(this).data('kanban');
        submitPallet(maguchiId, stepKanbanNo); // submitPallet can now be local
    });

    // Attach event handler for '-' button clicks (submitDepallet logic)
    $(document).on('click', '.submit-depallet', function() {
        const maguchiId = $(this).data('plat');
        const stepKanbanNo = $(this).data('kanban');
        submitDepallet(maguchiId, stepKanbanNo); // submitDepallet can now be local
    });
    
    // 定期実行 
    pageRefreshIntervalId = setInterval(refreshPage, 5000); 
    console.log("Automatic refresh started.");
        
    $('#refreshButton').on('click', function () {
        refreshPage();
    });

    /**
     * Updates the quantity input in the right-side card and the global data object.
     * @param {number} maguchiId - The Maguchi ID (1-4).
     * @param {number} newTakeCount - The new total take count.
     */
    function updateMaguchiInput(maguchiId, newTakeCount) {
        if (maguchiId >= 1 && maguchiId <= 4) {
            // Update the input field value
            $(`#count-input-${maguchiId}`).val(newTakeCount);

            // Update the global data object for submission
            if (maguchiInputData[maguchiId]) {
                maguchiInputData[maguchiId].take_count = newTakeCount;
            }
        }
    }

    /**
     * Collects the final data from the input cards and sends it to the backend.
     */
    function submitWorkCompletion() {
        const finalData = [];
        
        // Iterate through the stored data for Maguchi 1 through 4
        for (let id = 1; id <= 4; id++) {
            const data = maguchiInputData[id];
            
            // Only include entries that have a rack number assigned
            if (data && data.step_kanban_no && data.step_kanban_no !== 'N/A') {
                finalData.push({
                    maguchi_id: id,
                    step_kanban_no: data.step_kanban_no,
                    final_take_count: parseInt(data.take_count) // Ensure count is an integer
                });
            }
        }
    
        console.log("Final Data for Submission:", finalData);
    
    // TODO: Implement your actual AJAX/Fetch call to the backend API here
    // Example:
    /*
    $.ajax({
        url: '/api/complete_work',
        method: 'POST',
        contentType: 'application/json',
        data: JSON.stringify(finalData),
        success: function(response) {
            alert('作業完了しました！');
            // Reload or refresh the UI as needed
        },
        error: function(error) {
            console.error('Submission failed:', error);
            alert('作業完了に失敗しました。');
        }
    });
    */
    }

// Attach the function to the button click event
    $('#completeWorkButton').on('click', submitWorkCompletion);


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
        // let newTakeCount = currentTakeCount + 1; // No upper limit
        // Ensure we don't exceed the max value of 2
        let newTakeCount = Math.min(currentTakeCount + 1, 0); 
        
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
        // let newTakeCount = currentTakeCount - 1; // No lower limit
        // Ensure we don't go below the min value of -2
        let newTakeCount = Math.max(currentTakeCount - 1, -20);
        
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

        // 🛑 1. PAUSE THE AUTOMATIC REFRESH TIMER
        if (pageRefreshIntervalId) {
            clearInterval(pageRefreshIntervalId);
            pageRefreshIntervalId = null; // Clear the ID
            console.log("Automatic refresh paused for update.");
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
                    console.log("Success >> response.status:", response.message);

                    // 1. Update UI 
                    takeCountCell.text(newTakeCount);
                    
                    // 2. ⭐ UPDATE GLOBAL STORAGE HERE! ⭐
                    updateAMRDataStorage(maguchiId, stepKanbanNo, newTakeCount);
                    
                    showInfo("✅ Take count updated successfully!");
                    console.log("Take count updated successfully:", newTakeCount);
                } 
                // UPDATE value for 行き先
                refreshPage();
                // ⏱️ RESTART THE AUTOMATIC REFRESH TIMER
                pageRefreshIntervalId = setInterval(refreshPage, 5000);
                console.log("Update success. Automatic refresh restarted.");
            },
            error: function(jqXHR, textStatus, errorThrown) {
                // Try to get the specific message from the server response
                let errorMessage = "サーバーエラーが発生しました (Server error occurred).";
                console.error("Error updating take count >> Status:", jqXHR.status, errorMessage);

                if (jqXHR.responseJSON && jqXHR.responseJSON.message) {
                    errorMessage = jqXHR.responseJSON.message;
                } else if (jqXHR.responseText) {
                    // Fallback for non-JSON responses
                    errorMessage = jqXHR.responseText.substring(0, 100) + '...'; // Limit length
                }

                // ⏱️ RESTART THE AUTOMATIC REFRESH TIMER (even on error)
                pageRefreshIntervalId = setInterval(refreshPage, 5000);
                console.log("Update failed. Automatic refresh restarted.");

                alert(errorMessage);
            }
        });
    }

    // --- NEW HELPER FUNCTION TO UPDATE THE GLOBAL STORAGE ---
    function updateAMRDataStorage(maguchiId, kanbanNo, newTakeCount) {
        // 1. Convert maguchiId to string (Keys in the object are strings)
        const maguchiIdStr = String(maguchiId);
        
        // 2. RETRIEVE the data from Local Storage and PARSE it
        let storedData = localStorage.getItem("getAMRDataStorage");
        if (!storedData) {
            console.warn("Local Storage item 'getAMRDataStorage' not found.");
            return;
        }
        
        let getAMRDataStorage;
        try {
            getAMRDataStorage = JSON.parse(storedData);
        } catch (e) {
            console.error("Error parsing getAMRDataStorage from Local Storage:", e);
            return;
        }

        // 3. Check if the key (maguchiId) exists in the storage object
        if (getAMRDataStorage[maguchiIdStr]) {
            // The value should be an array of objects
            const itemArray = getAMRDataStorage[maguchiIdStr];
            
            // --- FIX for 'find is not a function' ---
            // Instead of .find(), use a standard for loop for better compatibility 
            // and to guarantee it works on objects that might look like arrays but aren't.
            let found = false;
            
            for (let i = 0; i < itemArray.length; i++) {
                const item = itemArray[i];
                
                if (item.step_kanban_no === kanbanNo) {
                    // Update the take_count property of the found item
                    item.take_count = String(newTakeCount); // Store as string
                    found = true;
                    break; // Stop loop once item is found and updated
                }
            }
            
            if (found) {
                // 4. ⭐ WRITE THE MODIFIED DATA BACK TO LOCAL STORAGE! ⭐
                localStorage.setItem("getAMRDataStorage", JSON.stringify(getAMRDataStorage));
                
                console.log(`Updated Local Storage for maguchi ${maguchiId} and kanban ${kanbanNo}. New take_count: ${newTakeCount}`);
            } else {
                console.warn(`Item not found in getAMRDataStorage for kanban_no: ${kanbanNo} under maguchi: ${maguchiIdStr}`);
            }
        } else {
            console.warn(`Maguchi ID not found in getAMRDataStorage: ${maguchiIdStr}`);
        }
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
});

function callAMRReturn() { 

    const params = new URLSearchParams(window.location.search);
    const buttonId = parseInt(params.get("id"));
    
    $.ajax({
        url: "/api/call_AMR_return",
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({
            button_id: buttonId 
        }),
        success: function(response) {
            if (response.status === "success") {
                confirm("✅ Bライン >> AMR return updated successfully!");
                console.log("Bライン >> AMR return updated successfully! Sent IDs:", buttonId);
            } else {
                alert(response.message || "更新に失敗しました (Update failed).");
                console.warn("Bライン >> AMR return Update failed:", response.message);
            }
        },
        error: function(xhr, status, error) {
            console.error("Error updating Bライン >> AMR return:", error);
            alert("Bライン AMR return>> サーバーエラーが発生しました.");
        }
    }); 
}


