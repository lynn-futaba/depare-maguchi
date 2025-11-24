
// common.js
function showInfo(message, duration = 100000) {
    let alertBox = document.getElementById("info-alert");
    if (!alertBox) {
        alertBox = document.createElement("div");
        alertBox.id = "info-alert";
        alertBox.style.cssText = `
            display:none;
            position:fixed;
            top:20px;
            right:20px;
            background:#2196F3;
            color:#fff;
            padding:15px 20px;
            border-radius:5px;
            font-size:16px;
            z-index:9999;
            box-shadow:0 2px 8px rgba(0,0,0,0.3);
        `;
        document.body.appendChild(alertBox);
    }

    alertBox.textContent = message;
    alertBox.style.display = "block";

    setTimeout(() => {
        alertBox.style.display = "none";
    }, duration);
}
