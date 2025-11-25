$(document).ready(function () {
 
    function refreshPage() {
    $.ajax({
        url: "/update_depallet_area",
        type: "GET",
        success: function (data) {
            // console.log('update_depallet_area >>', data); // TODO: testing
            // updateTable(data);
            updateDepalletArea(data);
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
    function updateTable(data) {

        const depalletArea = JSON.parse(data);
        const frontages = depalletArea.frontages;

            Object.keys(frontages).forEach(key => {
                // console.log('frontages >> key >>', frontages, key)

                const frontage = frontages[key];
                console.log('frontage　>>', frontage)
                
                // shelf.type ==1 for kotatsu　、if kotatsu, it includes inventories array
                
                // これだけ追加（または修正）すれば完璧！
                const index = parseInt(key);   // ← ここが最重要！！ // TODO: confrim the key, hard code
                // console.log('frontage >> index >>', index)
        
                const tableId  = `shelf-${index}`;
                const tabLabelId = `tab${index}-tab`;
                const tbody  = $(`#${tableId} tbody`);
                const maguchiNoLabel = $('#maguchi-no');
                const kotatsuNoLabel = $('#kotatsu-no');

                const thead  = $(`#${tableId} thead`);

                // if (thead.length === 0) return;
                if (tbody.length === 0) return;
                
                if (frontage.shelf == "None") {
                    return
                }
                // console.log(`Shelf for frontage ${frontage.shelf.type}`);

                if (frontage.shelf.type == 1) {
                    $(`#${tabLabelId}`).html(`間口${frontage.id}`).addClass('btn-success');
                    maguchiNoLabel.text(`対象 : 間口 ${frontage.id}`);
                    kotatsuNoLabel.text(`コタツ No : ${frontage.id}`);
                    thead.empty();
                    tbody.empty();
                    const row1 = `
                            <th>　</th>
                            <th>背番号</th>
                            <th>在庫数</th>
                            <th>取出数量</th>
                            <th>　</th>`;
                    thead.append(row1);
                    // console.log('inventories >>', Object.values(frontage.shelf.inventories));
                    Object.values(frontage.shelf.inventories).forEach(inv => {
                        const row = `
                            <tr>
                                <td><button onclick="pallet(${frontage.id}, '${inv.part.kanban_id}')"><b>＋<b></button></td>
                                <td>背番号 ${inv.part.kanban_id}</td>
                                <td>背番号 ${inv.part.kanban_id}</td> <!-- load_num -->
                                <td>背番号 ${inv.part.kanban_id}</td> <!-- signal category -->
                                <!--  <td>${inv.case_quantity}</td> -->
                                <td><button onclick="depallet(${frontage.id}, '${inv.part.kanban_id}')"><b>ー</b></button></td>
                            </tr>`;
                        tbody.append(row);
                    });
                } else {
                    $(`#${tabLabelId}`).html(`間口${frontage.id}`).removeClass('btn-success');
                    // console.log('Coming here >>>');
                    // Reset display for all non-Type 2 shelves
                    // $(`#${tabLabelId}`).text(key).removeClass('btn-success'); TODO: comment out

                    // 未使用
                    thead.empty();
                    tbody.empty();
                }
            });
    }
    
    
    // Track which maguchi IDs have data
    const maguchiHasData = {
        1: false,
        2: false,
        3: false,
        4: false,
        5: false
    };

    function updateDepalletArea(data) {
        const result = JSON.parse(data);
    
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
                maguchiNoLabel.text(`対象 : 間口 ${maguchiId}`);
                kotatsuNoLabel.text(`コタツ No : ${item.shelf_code}`);
                kanbanNoLabel.text(`かんばん No : ${item.step_kanban_no}`);
    
                tbody.append(`
                    <tr>
                        <td><button class="btn btn-success btn-sm" onclick="pallet(${maguchiId}, '${item.step_kanban_no}')">＋</button></td>
                        <td>${item.step_kanban_no}</td>
                        <td>${item.load_num}</td>
                        <td>${item.take_count}</td>
                        <td><button class="btn btn-danger btn-sm" onclick="depallet(${maguchiId}, '${item.step_kanban_no}')">ー</button></td>
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

//パレットおろし
function depallet(frontage_id,part_id) {
    $.ajax({
        url: "/to_flow_rack",
        type: "POST",
        contentType: "application/json",
        data: JSON.stringify({ "frontage_id": frontage_id,"part_id" :part_id }),
        success: function (data) {
            if (data["status"] === "success") {
                console.log('depallet >> to_flow_rack API', "OK");
            } else {
                alert("depalletizing error");
            }
        },
        error: function (error) {
            console.log('depallet >> to_flow_rack API >> Error', error.status + ": " + error.responseText);
            alert(error.status + ": " + error.responseText)
        }
    });
}
//パレット戻し, + plus
function pallet(frontage_id, part_id) {
    $.ajax({
        url: "/to_kotatsu",
        type: "POST",
        contentType: "application/json",
        data: JSON.stringify({ "frontage_id": frontage_id, "part_id": part_id }),
        success: function (data) {
            if (data["status"] === "success") {
                console.log('pallet >> to_kotatsu API', "OK");
            } else {
                alert("palletizing error");
            }
        },
        error: function (error) {
            console.log('pallet >> to_kotatsu API >> Error', error.status + ">> " + error.responseText);
            alert(error.status + ": " + error.responseText)
        }
    });
}

// コタツ返却. - minus
function returnKotatsu(id) {
    // const frontage_id = element.getAttribute("data-id"); TODO: comment out
    console.log('returnKotatsu >>', id);
    const frontage_id = id;
    const result = confirm(`間口 ${frontage_id}のコタツを返却します`);

    if (result) {
        $.ajax({
            url: "/return_kotatsu",
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
