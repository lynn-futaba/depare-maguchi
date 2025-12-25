let getAMRDataStorage = {}
// ⭐ Define a global variable to hold the timer ID
let pageRefreshIntervalId;

$(document).ready(function () {
 
    function refreshPage() {
        console.log("Page refreshed automatically.");

        const params = new URLSearchParams(window.location.search);
        const idValue = parseInt(params.get("id"));
        const nameValue = params.get("name");

        if (nameValue.includes("R1")) {
            document.getElementById("layout-R1").style.display = "block";
            document.getElementById("layout-R2").style.display = "none";
            document.getElementById("layout-R3").style.display = "none";
            document.getElementById("layout-L1").style.display = "none";
            document.getElementById("layout-L2").style.display = "none";
            document.getElementById("layout-L3").style.display = "none";
            
        } 
        else if (nameValue.includes("R2")) {
            document.getElementById("layout-R1").style.display = "none";
            document.getElementById("layout-R2").style.display = "block";
            document.getElementById("layout-R3").style.display = "none";
            document.getElementById("layout-L1").style.display = "none";
            document.getElementById("layout-L2").style.display = "none";
            document.getElementById("layout-L3").style.display = "none";
        }
        else if (nameValue.includes("R3")) {
            document.getElementById("layout-R1").style.display = "none";
            document.getElementById("layout-R2").style.display = "none";
            document.getElementById("layout-R3").style.display = "block";
            document.getElementById("layout-L1").style.display = "none";
            document.getElementById("layout-L2").style.display = "none";
            document.getElementById("layout-L3").style.display = "none";
        }

        else if (nameValue.includes("L1")) {
            document.getElementById("layout-R1").style.display = "none";
            document.getElementById("layout-R2").style.display = "none";
            document.getElementById("layout-R3").style.display = "none";
            document.getElementById("layout-L1").style.display = "block";
            document.getElementById("layout-L2").style.display = "none";
            document.getElementById("layout-L3").style.display = "none";
        }

        else if (nameValue.includes("L2")) {
            document.getElementById("layout-R1").style.display = "none";
            document.getElementById("layout-R2").style.display = "none";
            document.getElementById("layout-R3").style.display = "none";
            document.getElementById("layout-L1").style.display = "none";
            document.getElementById("layout-L2").style.display = "block";
            document.getElementById("layout-L3").style.display = "none";
        }

        else if (nameValue.includes("L3")) {
            document.getElementById("layout-R1").style.display = "none";
            document.getElementById("layout-R2").style.display = "none";
            document.getElementById("layout-R3").style.display = "none";
            document.getElementById("layout-L1").style.display = "none";
            document.getElementById("layout-L2").style.display = "none";
            document.getElementById("layout-L3").style.display = "block";
        }
        
        else {
            document.getElementById("layout-R1").style.display = "none";
            document.getElementById("layout-R2").style.display = "none";
            document.getElementById("layout-R3").style.display = "none";
            document.getElementById("layout-L1").style.display = "none";
            document.getElementById("layout-L2").style.display = "none";
            document.getElementById("layout-L3").style.display = "none";
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

        // --- GLOBAL CONFIGURATION (Safe Fallbacks) ---
        let globalButtonIdMap = { };

        let globalShelfMap = { };

        // --- SYNC FUNCTION ---
        async function syncUIConfig() {
            try {
                const response = await fetch('/api/get_a_ui_config');
                const config = await response.json();
                
                if (config.buttonIdMap && config.shelfMap) {
                    globalButtonIdMap = config.buttonIdMap;
                    globalShelfMap = config.shelfMap;
                    console.log("✅ UI Config synchronized with app_config.json");
                }
            } catch (error) {
                console.warn("⚠️ Using hardcoded UI defaults (API unavailable)");
            }
        }

        // Run sync immediately on load
        syncUIConfig();

        function getDepalletAreaByPlat(data, idValue, nameValue) {
            const result = JSON.parse(data);
             // 1. Button → Plat (Data Source) mapping
            // const buttonIdMap = { 
            //     7: [24, 23, 22, 21, 20], // R1, Aライン, 間口[5,4,3,2,1] , フローラック➞1
            //     8: [24, 23, 22, 21, 20], // R2, Aライン, 間口[5,4,3,2,1], フローラック➞1
            //     9: [24, 23, 22],         // R3, Aライン, 間口[5,4,3], フローラック➞5
            //     10: [24, 23, 22, 21, 20],// L1, Aライン, 間口[5,4,3,2,1] フローラック➞5
            //     11: [24, 23, 22, 21, 20],// L2, Aライン, 間口[5,4,3,2,1] フローラック➞5
            //     12: [22, 21, 20]         // L3, Aライン, 間口[3,2,1] フローラック➞1
            // };
        
            // // 2. Button → Shelf IDs (Display UI) mapping
            // const shelfMap = {
            //     7:  [5, 4, 3, 2, 1],
            //     8:  [5, 4, 3, 2, 1],
            //     9:  [5, 4, 3],
            //     10: [5, 4, 3, 2, 1],
            //     11: [5, 4, 3, 2, 1],
            //     12: [3, 2, 1]
            // };

            const targetPlats = globalButtonIdMap[idValue] || [];
            const targetShelves = globalShelfMap[idValue] || [];
        
            document.getElementById("frontageName").textContent = 'デパレ間口 <' + nameValue + '>';
        
            targetShelves.forEach((shelfNum, shelfIndex) => {
                const platId = targetPlats[shelfIndex];
                const items = result[platId] || [];
                const shelfId = `#shelf-${shelfNum}`;
                const tbody = $(`${shelfId} tbody`);
                const thead = $(`${shelfId} thead`);
                let cardId = `#card${shelfNum}`;
                let cardNo = $(`${cardId} tbody`);
        
                // --- FLASH PREVENTION ---
                // If the table header already exists, don't clear everything. 
                // Just update the specific values.
                // if (thead.children().length > 0 && items.length > 0) {
                //     items.forEach((item) => {
                //         const stepKanbanNo = item.step_kanban_no ?? '-';
                //         const rowId = `row-${platId}-${stepKanbanNo}`;
                        
                //         // Only update the numbers, don't re-draw the whole row
                //         $(`#take-count-${rowId}`).text(item.take_count ?? 0);
                //         // Update stock/load num
                //         $(`#${rowId} td:nth-child(3)`).text(item.load_num ?? 0); 
                //     });
                //     return; // Skip the rest of the function (no flashing!)
                // }
        
                // --- INITIAL DRAW (Only happens once or when button changes) ---
                thead.empty();
                tbody.empty();
                cardNo.empty();
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

                    // UPDATE value for 行き先
                    refreshPage();
                    
                    // 2. ⭐ UPDATE GLOBAL STORAGE HERE! ⭐
                    updateAMRDataStorage(maguchiId, stepKanbanNo, newTakeCount);
                    
                    showInfo("✅ 取出数量を更新しました!");
                    console.log("取出数量を更新しました！:", newTakeCount);
                } 
                
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

function callAMRReturn() { // You can define it like this to ensure it's global

    const params = new URLSearchParams(window.location.search);
    const buttonId = parseInt(params.get("id"));

    // --- 1. Start Loading State ---
    const $btn = $("#btnAMRReturn");
    const $spinner = $("#spinnerAMRReturn");
    
    $btn.prop("disabled", true);      // Disable button to prevent double-clicks
    $spinner.removeClass("d-none");   // Show spinner
        
    $.ajax({
        url: "/api/call_AMR_return",
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({
            button_id: buttonId
        }),
        success: function(response) {
            if (response.status === "success") {
                alert("✅ Aライン >> 全作業完了しました！");
                console.log("Aライン >> 全作業完了しました！ Sent IDs:", buttonId);
              
              // 2. Small timeout ensures the alert is dismissed before closing
                setTimeout(function() {
                    window.close();
                }, 100);
                        
            } else {
                alert(response.message || "全作業失敗しました (Update failed).");
                console.warn("Aライン >> 全作業失敗しました:", response.message);
            }
        },
        error: function(xhr, status, error) {
            console.error("Aライン >> 全作業失敗しました:", error);
            alert("Aライン >> 全作業失敗しました (Server error occurred).");
        },
        complete: function() {
            // --- 2. Stop Loading State ---
            // This runs regardless of success or error
            $btn.prop("disabled", false);
            $spinner.addClass("d-none");
        }
    });
}

function callAMRFlowrackOnly() { 

    const params = new URLSearchParams(window.location.search);
    const buttonId = parseInt(params.get("id"));

    // UI Elements
    const $btn = $("#btnAMRFlowrack");
    const $spinner = $("#spinnerAMRFlowrack");

    // 1. Enter Loading State
    $btn.prop("disabled", true);
    $spinner.removeClass("d-none");
    
    $.ajax({
        url: "/api/call_AMR_flowrack_only",
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({
            button_id: buttonId 
        }),
        success: function(response) {
            if (response.status === "success") {
                confirm("✅ Aライン >> フローラック単体発進に成功しました!");
                console.log("Aライン >> フローラック単体発進に成功しました! Sent IDs:", buttonId);
            } else {
                alert(response.message || "更新に失敗しました (Update failed).");
                console.warn("Aライン >> フローラック単体発進 return Update failed:", response.message);
            }
        },
        error: function(xhr, status, error) {
            console.error("Error updating Aライン >> フローラック単体発進 return:", error);
            alert("Aライン フローラック単体発進 return>> サーバーエラーが発生しました.");
        },
        complete: function() {
            // 2. Exit Loading State (always runs)
            $btn.prop("disabled", false);
            $spinner.addClass("d-none");
        }
    }); 
}