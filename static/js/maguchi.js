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
            const frontages = depalletArea["frontages"];
        
            Object.keys(frontages).forEach((key, index) => {
                const tableId   = `shelf-${index}`;          // 0‑based index
                const tbody     = $(`#${tableId} tbody`);
                const tabLabelId = `tab${index}-tab`;

                console.log('tableId', tableId)
                console.log('tbody', tbody)
                console.log('tabLabelId', tabLabelId)
        
                const frontage = frontages[key];
        
                // ---- skip empty shelf ------------------------------------------------
                if (!frontage.shelf || frontage.shelf === "None") return;
                if (frontage.shelf.type !== 1) return;
        
                // ---- update tab label -------------------------------------------------
                $(`#${tabLabelId}`)
                    .text(`間口${frontage.id}取出`)
                    .attr('data-id', frontage.id)
                    .addClass('btn-success');   // highlight active frontage
        
                // ---- fill table -------------------------------------------------------
                Object.keys(frontage.shelf.inventories).forEach(invKey => {
                    const inv = frontage.shelf.inventories[invKey];
                    const row = `
                        <tr>
                            <td><button onclick="Pallet(${frontage.id}, '${inv.part.kanban_id}')">＋</button></td>
                            <td>${inv.part.kanban_id}</td>
                            <td>${inv.case_quantity}</td>
                            <td><button onclick="Depallet(${frontage.id}, '${inv.part.kanban_id}')">ー</button></td>
                        </tr>`;
                    tbody.append(row);
                });
            });
        }
    };

    // 定期実行 
    setInterval(refreshPage, 500);
    // setInterval(refreshPage, 50000); TODO: added
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