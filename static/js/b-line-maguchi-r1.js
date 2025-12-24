let getAMRDataStorage = {}
// ⭐ Define a global variable to hold the timer ID
let pageRefreshIntervalId;

$(document).ready(function () {
 
    function refreshPage() {
        console.log("Page refreshed automatically.");
        const params = new URLSearchParams(window.location.search);
        const idValue = parseInt(params.get("id"));
        const nameValue = params.get("name");

        $.ajax({
            url: "/api/get_depallet_area_by_plat",
            type: "POST",
            contentType: 'application/json',
            data: JSON.stringify({
                button_id: idValue 
            }),
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
                const response = await fetch('/api/get_b_ui_config');
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

        /**
 * Updates the UI based on incoming JSON data.
 * Prevents flashing by only updating text nodes if values have changed.
 */
function getDepalletAreaByPlat(data, idValue, nameValue) {
    const result = JSON.parse(data);
    const targetPlats = globalButtonIdMap[idValue] || [];
    const targetShelves = globalShelfMap[idValue] || [];
    
    // Select main wrappers
    const maguchiWrapper = document.getElementById("maguchiCards");
    const flowWrapper = document.getElementById("flowRackWrapper");
    
    // Select inner containers where cards are injected
    const maguchiContainer = document.getElementById("maguchiDynamicContainer");
    const flowContainer = document.getElementById("flowRackDynamicContainer");

    // 2. Structural Check: Rebuild UI only if the button ID changed
    const currentViewId = maguchiWrapper.getAttribute("data-current-view");
    const isNewView = currentViewId !== String(idValue);

    if (isNewView) {
        // Build Main Cards (Left Side)
        renderMaguchiStructure(maguchiContainer, targetShelves);
        // Build Flow Rack Cards (Right Side - ②③④⑤)
        renderFlowRackStructure(flowContainer, targetShelves);
        
        // Mark current view state
        maguchiWrapper.setAttribute("data-current-view", idValue);
        if (flowWrapper) flowWrapper.setAttribute("data-current-view", idValue);
    }

    // 3. Update Values (No-Flash Logic)
    targetShelves.forEach((shelfNum, shelfIndex) => {
        const platId = targetPlats[shelfIndex];
        const items = result[platId] || [];
        
        // Get Table Body references
        const tbodyMaguchi = document.querySelector(`#shelf-${shelfNum} tbody`);
        const tbodyFlow = document.querySelector(`#flow-tbody-${shelfNum}`);

        // Handle "No Data" state
        if (items.length === 0) {
            handleNoData(tbodyMaguchi, `間口${shelfNum}: データなし`, 5);
            handleNoData(tbodyFlow, `データなし`, 2);
            return;
        }

        // Iterate through items and update rows
        items.forEach((item) => {
            const stepKanbanNo = item.step_kanban_no ?? '-';
            const loadNum = String(item.load_num ?? 0);
            const takeCount = String(item.take_count ?? 0);

            // --- Update Maguchi Table ---
            updateOrCreateRow(tbodyMaguchi, `row-${platId}-${stepKanbanNo}`, platId, stepKanbanNo, loadNum, takeCount, "maguchi");

            // --- Update Flow Rack Table ---
            updateOrCreateRow(tbodyFlow, `flow-row-${platId}-${stepKanbanNo}`, platId, stepKanbanNo, loadNum, takeCount, "flow");
        });
    });
}

/**
 * Logic to update existing text or append new rows if missing
 */
function updateOrCreateRow(tbody, rowId, platId, kanban, load, take, type) {
    let row = document.getElementById(rowId);

    if (row) {
        // UPDATE: Only change text if it's different to prevent flashing
        if (type === "maguchi") {
            if (row.cells[2].textContent !== load) row.cells[2].textContent = load;
            const takeCell = document.getElementById(`take-count-${rowId}`);
            if (takeCell && takeCell.textContent !== take) takeCell.textContent = take;
        } else {
            if (row.cells[1].textContent !== take) row.cells[1].textContent = take;
        }
    } else {
        // CREATE: Append if not found
        if (tbody.innerText.includes("データなし")) tbody.innerHTML = "";
        
        const html = (type === "maguchi") 
            ? `<tr id="${rowId}">
                <td><button class="btn btn-success btn-sm submit-pallet" data-plat="${platId}" data-kanban="${kanban}">＋</button></td>
                <td>${kanban}</td>
                <td class="fw-bold">${load}</td>
                <td id="take-count-${rowId}" class="fw-bold">${take}</td>
                <td><button class="btn btn-danger btn-sm submit-depallet" data-plat="${platId}" data-kanban="${kanban}">ー</button></td>
               </tr>`
            : `<tr id="${rowId}"><td>${kanban}</td><td class="fw-bold">${take}</td></tr>`;
            
        $(tbody).append(html);
    }
}

/**
 * Re-renders the Main Card column (1 column layout)
 */
function renderMaguchiStructure(container, shelves) {
    container.innerHTML = ''; 
    shelves.forEach(num => {
        container.insertAdjacentHTML('beforeend', `
            <div class="card mb-3">
                <div class="card-header text-center text-white bg-primary"><b>間口${num}</b></div>
                <div class="card-body p-0">
                    <table class="table table-bordered mb-0 text-center" id="shelf-${num}">
                        <thead class="table-secondary">
                            <tr><th></th><th>背番号</th><th>在庫数</th><th>取出数量</th><th></th></tr>
                        </thead>
                        <tbody></tbody>
                    </table>
                </div>
            </div>`);
    });
}

/**
 * Re-renders the Flow Rack column (2 column grid: ②③ / ④⑤)
 */
function renderFlowRackStructure(container, shelves) {
    container.innerHTML = '';
    const circleMap = { 1: "①", 2: "②", 3: "③", 4: "④", 5: "⑤" };
    
    // Filter out the shelf with value 1
    const filteredShelves = shelves.filter(num => num !== 1);

    let gridHtml = '<div class="row g-3">';

    filteredShelves.forEach((num, index) => {
        // Create a new row after every 2 items
        if (index > 0 && index % 2 === 0) {
            gridHtml += '</div><div class="row g-3 mt-1">';
        }

        gridHtml += `
            <div class="col-md-6">
                <div class="card shadow">
                    <div class="card-header text-white text-center fw-bold bg-primary">${circleMap[num] || num}</div>
                    <div class="card-body p-0">
                        <table class="table table-bordered mb-0 text-center">
                            <thead class="table-light"><tr><th>背番号</th><th>取出数量</th></tr></thead>
                            <tbody id="flow-tbody-${num}"></tbody>
                        </table>
                    </div>
                </div>
            </div>`;
    });

    container.innerHTML = gridHtml + '</div>';
}

/**
 * Simple helper for No Data messages
 */
function handleNoData(tbody, msg, colspan) {
    if (tbody && !tbody.innerHTML.includes(msg)) {
        tbody.innerHTML = `<tr><td colspan="${colspan}" class="p-3 text-danger text-center">${msg}</td></tr>`;
    }
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
                    
                    showInfo("✅ 取出数量を更新しました！");
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
                confirm("✅ Bライン >> AMRの呼び出しに成功しました！");
                console.log("Bライン >> AMRの呼び出しに成功しました！ Sent IDs:", buttonId);
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


