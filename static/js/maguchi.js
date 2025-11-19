$(document).ready(function () {
 
    function refreshPage() {
        $.ajax({
            url: "/update_depallet_area",
            type: "GET",
            success: function (data) {
                console.log('update_depallet_area >>', data);
                updateTable(data);
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
                
        //         let tbody = $(`#${index} tbody`);
                   
        //         tbody.empty();
        //         let frontage = frontages[key];
                
        //         if (frontage.shelf == "None") {
        //             return;
        //         }
        //         if (frontage.shelf.type == 1) {
        //             Object.keys(frontage.shelf.inventories).forEach((key) => {

        //                 let tab =$(`#tab${index}`).contents().filter(function () {
        //                     return this.nodeType === 3;
        //                 }).first()
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

        function updateTable(data) {
            const depalletArea = JSON.parse(data);
            const frontages = depalletArea.frontages;
        
            Object.keys(frontages).forEach(key => {
                const frontage = frontages[key];
        
                // これだけ追加（または修正）すれば完璧！
                const index = parseInt(key) - 1;   // ← ここが最重要！！
        
                const tableId    = `shelf-${index}`;
                const tabLabelId = `tab${index}-tab`;
                const tbody      = $(`#${tableId} tbody`);
        
                if (tbody.length === 0) return;
        
                // 以下は今まで通り（空棚のときはクリアする処理も入れた方が親切）
                if (!frontage.shelf || frontage.shelf === "None" || frontage.shelf.type !== 1) {
                    console.log('Shelf is None >>>');
                    $(`#${tabLabelId}`).text(index < 4 ? `間口${key}` : "取出").removeClass('btn-success');
                    tbody.empty();
                    return;
                }
        
                $(`#${tabLabelId}`).text(`間口${key}取出`).addClass('btn-success');
                tbody.empty();
        
                Object.values(frontage.shelf.inventories).forEach(inv => {
                    const row = `<tr>
                        <td><button onclick="Pallet(${key}, '${inv.part.kanban_id}')">＋</button></td>
                        <td>${inv.part.kanban_id}</td>
                        <td>${inv.case_quantity}</td>
                        <td><button onclick="Depallet(${key}, '${inv.part.kanban_id}')">ー</button></td>
                    </tr>`;
                    tbody.append(row);
                });
            });
        }
    };

    // 定期実行 
    // setInterval(refreshPage, 500);
    setInterval(refreshPage, 5000); // TODO: added
});

//パレットおろし
function Depallet(frontage_id,part_id) {
    $.ajax({
        url: "/to_flow_rack",
        type: "POST",
        contentType: "application/json",
        data: JSON.stringify({ "frontage_id": frontage_id,"part_id" :part_id }),
        success: function (data) {
            if (data["status"] === "success") {
                console.log("OK");
              
            } else {
                alert("depalletizing error");
            }
        },
        error: function (error) {

            alert(error.status + ": " + error.responseText)
        }
    });
}
//パレット戻し
function Pallet(frontage_id, part_id) {
    $.ajax({
        url: "/to_kotatsu",
        type: "POST",
        contentType: "application/json",
        data: JSON.stringify({ "frontage_id": frontage_id, "part_id": part_id }),
        success: function (data) {
            if (data["status"] === "success") {
                console.log("OK");

            } else {
                alert("palletizing error");
            }
        },
        error: function (error) {
  
            alert(error.status + ": " + error.responseText)
        }
    });
}

// コタツ返却
function ReturnKotatsu(element) {
    console.log(element);
    const frontage_id = element.getAttribute("data-id");
    console.log(frontage_id);

    const result = confirm(`間口 ${frontage_id}のコタツを返却します`);

    if (result) {
        $.ajax({
            url: "/return_kotatsu",
            type: "POST",
            contentType: "application/json",
            data: JSON.stringify({ "frontage_id": frontage_id}),
            success: function (data) {
                if (data["status"] === "success") {
                    console.log("OK");

                } else {
                    alert("error");
                }
            },
            error: function (error) {

                alert(error.status + ": " + error.responseText)
            }
        });
    }     
}